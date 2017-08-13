def cmd(cmd, stop=False):
    def wrapped(event):
        if stop:
            event.stop()
        return cmd
    return wrapped


class CommandsController(object):
    def __init__(self):
        self._times = {}

    def command_decorator(self, threshold=None):
        def decorator(fn):
            def wrapped(event):
                if threshold:
                    prevtime = self._times.get(event.code)
                    delay = event.time-prevtime if prevtime else None
                if not threshold or delay is None or delay>threshold:
                    out = fn(event)
                    self._times[event.code] = event.time
                    return out or []
                else:
                    return []
            return wrapped
        return decorator


_ctrl = CommandsController()
command = _ctrl.command_decorator


def knob(x):
    return command(threshold=0.25)(x)


def slider(x):
    return command(threshold=0.05)(x)


def zoom_in(event):
    return ZOOM_IN*(int(event.delta/5)+1)


def zoom_out(event):
    return ZOOM_OUT*(int(event.delta/5)+1)


def do_scrub(cmds):
    def scrub(event):
        if 'scrub' not in event.modifiers:
            return cmds
    return scrub


@command(threshold=0.05)
def scrub_left(ev):
    return do_scrub(
        ['keydown Control_L', 'str j', 'keyup Control_L'])


@command(threshold=0.05)
def scrub_right(ev):
    return do_scrub(
        ['keydown Control_L', 'str l', 'keyup Control_L'])


@command(threshold=0.1)
def frames_left(event):
    delta = abs(event.delta)
    if delta<5:
        return REVERSE_NUDGE # * delta
    else:
        return NUDGE_10_BACKWARD # * (int(delta-10/4)+1)


@command(threshold=0.1)
def frames_right(event):
    delta = abs(event.delta)
    if delta<5:
        return FORWARD_NUDGE # * delta
    else:
        return NUDGE_10_FORWARD # * (int(delta-10/4)+1)


def addmodifier(ctrl, x):
    @command()
    def wrapped(event):
        ctrl.enable_modifier(x)
    return wrapped


def remmodifier(crel, x):
    @command()
    def wrapped(event):
        if x in event.modifiers:
            ctrl.disable_modifier(x)
    return wrapped


def ifmod(mod, enabled, disabled=None):
    def wrapped(event):
        if mod in event.modifiers:
            return enabled
        else:
            return disabled or []
    return wrapped


def ifnotmod(mod, enabled, disabled=None):
    def wrapped(event):
        if mod not in event.modifiers:
            return enabled
        else:
            return disabled or []
    return wrapped


LEFT = 'key a'
RIGHT = 'key s'
MARK_IN = 'key i'
MARK_OUT = 'key o'
MARK_CLIP = 'str ]'
BIN_PREV = ['keydown Alt_L', 'str q', 'keyup Alt_L'] 
BIN_PREV_IN_GROUP = [
        'keydown Alt_L', 'keydown Shift_L',
        'str q', 'keyup Alt_L', 'keyup Shift_L'] 
BIN_NEXT = ['keydown Alt_L', 'str w', 'keyup Alt_L']
BIN_NEXT_IN_GROUP = [
        'keydown Alt_L', 'keydown Shift_L',
        'str w', 'keyup Alt_L', 'keyup Shift_L'] 
TILE_TO_VIEWER = ['keydown Control_L', 'key Return', 'keyup Control_L']
REVERSE_NUDGE = ['key Left']
FORWARD_NUDGE = ['key Right']
NUDGE_10_BACKWARD = ['key m']
NUDGE_10_FORWARD = ['str /']
FULLSCREEN_TOGGLE = ['key F12']
PLAY = ['keydown Control_L', 'key p', 'keyup Control_L']
STOP = ['key k']
TOGGLE_PLAY = ['key Space']
GOTO_MARK_IN = [
        'keydown Control_L', 'key i', 'keyup Control_L']
GOTO_MARK_OUT = [
        'keydown Control_L', 'key o', 'keyup Control_L']
SWITCH = ['key Tab']
JOIN = ['key Escape']
UNMARK = ['key p']
JOG = ['keydown Control_L', 'key k', 'keyup Control_L']
PREVIEW = ['keydown Alt_L', 'key l', 'keyup Alt_L']
HOME = ['key h']
END = ['key colon']
INSERT = ['key v']
REPLACE = ['key b']
EMPTY_CUT = ['key c']
ZOOM_IN = ['str =']
ZOOM_OUT = ['str -']
DISABLE_ALL_TRACKS = ['str ~']
TOGGLE_V1 = ['key 1']
TOGGLE_V2 = ['key 2']
TOGGLE_A1 = ['key 3']
TOGGLE_A2 = ['key 4']
TOGGLE_A3 = ['key 5']
TOGGLE_A4 = ['key 6']
TOGGLE_A5 = ['key 7']
TOGGLE_A6 = ['key 8']
TOGGLE_A7 = ['key 9']
DELETE = ['key x']
REMOVE = ['key z']
CLOSE_ALL_GAPS = ['keydown Alt_L', 'str X', 'keyup Alt_L']
UNDO = ['keydown Control_L', 'key z', 'keyup Control_L']
REDO = ['keydown Control_L', 'key y', 'keyup Control_L']
