import os
from subprocess import Popen, PIPE
from .events import (
        EventsManager, Event,
        EV_KEYUP, EV_KEYDOWN, EV_SLIDE)
from .utils import debug
from . import x11


class Controller(object):
    def __init__(self, keyboard, target_window_name=None):
        self.keyboard = keyboard
        self.target_window_name = target_window_name

        def parse_and_send_commands(event, cmds):
            self.send_commands(self.parse_cmds(cmds, event))

        self.event_manager = EventsManager(callback=parse_and_send_commands)

        FNULL = open(os.devnull, 'w')
        self.xte = Popen(['xte'], stdin=PIPE, stdout=FNULL)

    @property
    def modifiers(self):
        return list(map(lambda x: x[0], filter(
                lambda x: x[1], self.event_manager._modifiers.items())))

    def enable_modifier(self, modifier):
        self.event_manager._modifiers[modifier] = True

    def disable_modifier(self, modifier):
        self.event_manager._modifiers[modifier] = False

    def handle_midi_event(self, midi_event, data=None):
        code = midi_event.getControllerNumber()
        val = midi_event.getControllerValue()

        if self.is_button(code):
            event = Event(
                    EV_KEYDOWN if val > 0 else EV_KEYUP,
                    value=int(val>0), code=code)
        else:
            event = Event(EV_SLIDE, value=val, code=code)
        
        self.event_manager.emit(event)
        self.event_manager.update()

    def send_commands(self, cmds):
        if cmds:
            debug("COMMANDS: %s" % cmds)

        if (not self.target_window_name or
                x11.is_window_in_focus(self.target_window_name)):
            for cmd in cmds:
                self.xte.stdin.write((cmd+'\n').encode())
                self.xte.stdin.flush()

    def parse_cmds(self, cmds, event):
        if callable(cmds):
            cmds = self.parse_cmds(cmds(event), event)

        if isinstance(cmds, str):
            cmds = [cmds]

        out = []
        for cmd in cmds:
            if callable(cmd):
                cmd = cmd(event)
            if isinstance(cmd, (list, tuple)):
                out += self.parse_cmds(cmd, event)
            else:
                out.append(cmd)
        return out

    def run(self):
        self.event_manager.loop()

    def keyup(self, *args, **kwargs):
        self.event_manager.keyup(*args, **kwargs)

    def keydown(self, *args, **kwargs):
        self.event_manager.keydown(*args, **kwargs)

    def slideup(self, *args, **kwargs):
        self.event_manager.slideup(*args, **kwargs)

    def slidedown(self, *args, **kwargs):
        self.event_manager.slidedown(*args, **kwargs)

    def longpress(self, *args, **kwargs):
        self.event_manager.longpress(*args, **kwargs)

    def doublehit(self, *args, **kwargs):
        self.event_manager.doublehit(*args, **kwargs)

    def is_button(self, code):
        return self.keyboard.is_button(code)
