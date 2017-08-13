import time
from collections import defaultdict
from .commands import cmd
from .utils import debug


EV_KEYUP = 'keyup'
EV_SLIDE = 'slide'
EV_SLIDEUP = 'slideup'
EV_SLIDEDOWN = 'slidedown'
EV_KEYDOWN = 'keydown'
EV_LONGPRESS = 'longpress'
EV_DOUBLEHIT = 'doublehit'


class Event(object):
    def __init__(self, event_type, code, value, delay=None, delta=None, event_time=None):
        self._type = event_type
        self.time = event_time or time.time()
        self.code = code
        self.value = value
        self.delay = delay
        self.delta = delta
        self.stopped = False
        self.presstime = 0
        self._emitted = False
        self.modifiers = []

    def clone(self, new_type=None):
        return Event(
                new_type or self._type, self.code, self.value,
                delay=self.delay, delta=self.delta)

    @property
    def type(self):
        return self._type

    @property
    def emitted(self):
        return self._emitted

    def stop(self):
        self.stopped = True

    def __repr__(self):
        delay = str(round(self.delay, 10) if self.delay is not None else '-').ljust(12)
        return '<%s: code=%s val=%s delay=%s delta=%s, modifiers=%s>' % (
                self.type.upper().ljust(10), str(self.code).ljust(3), str(self.value).ljust(3),
                delay, str(self.delta if self.delta is not None else '-').ljust(4),
                ', '.join(self.modifiers))


class EventsManager(object):
    def __init__(self, longpress_time=0.25, doublehit_time=0.25, callback=None):

        def print_handler_callback(event, handler):
            print(handler)

        self.longpress_time = longpress_time
        self.doublehit_time = doublehit_time
        self._handler_callback = callback or print_handler_callback
        self._handlers = defaultdict(lambda: defaultdict(list))
        self._forced_handlers = defaultdict(lambda: defaultdict(list))
        self._queue = []
        self._keydowns = {}
        self._longpress = {}
        self._prevhits = defaultdict(dict)
        self._modifiers = {}

    def register(self, event_type, code, *cmds, always=False):
        all_cmds = []
        for subcmds in cmds:
            if isinstance(subcmds, (list, tuple)):
                all_cmds += subcmds
            else:
                all_cmds.append(subcmds)

        if always:
            self._forced_handlers[event_type][code] += all_cmds
        else:
            self._handlers[event_type][code] += all_cmds

    def register_modifier(self, code, name):
        def activate_modifier(event):
            self._modifiers[name] = True
            return []

        def deactivate_modifier(event):
            self._modifiers[name] = False
            return []

        self._modifiers[name] = False

        self.keydown(code, activate_modifier, always=True)
        self.keyup(code, deactivate_modifier, always=True)

    def keyup(self, code, *cmds, **kw):
        self.register(EV_KEYUP, code, *cmds, **kw)

    def keydown(self, code, *cmds, **kw):
        self.register(EV_KEYDOWN, code, *cmds, **kw)

    def longpress(self, code, *cmds, stop=True, **kw):
        if stop:
            cmds = map(lambda x: cmd(x, stop=True), cmds)
        self.register(EV_LONGPRESS, code, *cmds, **kw)
        self.keydown(code, self._start_longpress, always=True)

    def doublehit(self, code, *cmds, stop=True, **kw):
        if stop:
            cmds = map(lambda x: cmd(x, stop=True), cmds)
        self.register(EV_DOUBLEHIT, code, *cmds, **kw)

    def slideup(self, code, *cmds, **kw):
        self.register(EV_SLIDEUP, code, *cmds, **kw)

    def slidedown(self, code, *cmds, **kw):
        self.register(EV_SLIDEDOWN, code, *cmds, **kw)

    def dispatch(self, event):
        event.modifiers = list(map(
                lambda x: x[0], filter(
                    lambda x: x[1], self._modifiers.items())))
        new_events = False

        if event.type == EV_KEYDOWN:
            self._keydowns[event.code] = event
        elif event.type == EV_KEYUP:
            old = self._keydowns.pop(event.code, None)
            if old and old.stopped:
                return

        self._calc_delta(event)

        if event.type == EV_KEYDOWN:
            if event.delay and event.delay <= self.doublehit_time:
                new_event = event.clone(EV_DOUBLEHIT)
                self._calc_delta(new_event)
                self.emit(new_event)
                new_events = True
        elif event.type == EV_SLIDE:
            if event.delta is not None:
                if event.delta < 0:
                    new_event = event.clone(EV_SLIDEDOWN)
                else:
                    new_event = event.clone(EV_SLIDEUP)
                self.emit(new_event)
                new_events = True

        debug(event)

        cmds_list = self._handlers[event.type][event.code]
        for cmds in cmds_list:
            self._handler_callback(event, cmds)
        if event.stopped and event.code in self._keydowns:
            self._keydowns[event.code].stopped = True

        return new_events

    def dispatch_always(self, event):
        cmds_list = self._forced_handlers[event.type][event.code]
        for cmds in cmds_list:
            self._handler_callback(event, cmds)

    def emit(self, event):
        if not event.emitted:
            event._emitted = True
            self._queue.insert(0, event)

    def update(self):
        try:
            event = self._queue.pop()
        except IndexError:
            pass
        else:
            if not event.stopped:
                if self.dispatch(event):
                    self.update()
            self.dispatch_always(event)
        self._handle_longpress()

    def _calc_delta(self, event):
        evtype = event.type
        try:
            prevtime, prevvalue = self._prevhits[evtype][event.code]
        except KeyError:
            prevtime, prevvalue = None, None
        else:
            event.delta = event.value - prevvalue
            event.delay = event.time - prevtime
        finally:
            self._prevhits[evtype][event.code] = (event.time, event.value)

    def _start_longpress(self, event):
        def wrapped(event):
            self._longpress[event.code] = event
            return []
        return wrapped

    def _handle_longpress(self):
        curtime = time.time()

        for key, event in dict(self._longpress).items():
            if event.code in self._keydowns:
                if curtime - event.time > self.longpress_time:
                    self._longpress.pop(key)
                    new_event = event.clone(EV_LONGPRESS)
                    self.emit(new_event)
            else:
                self._longpress.pop(key)

    def loop(self):
        while True:
            self.update()
            time.sleep(0.1)
