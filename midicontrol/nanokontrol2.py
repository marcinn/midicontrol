from .controller import Controller
from . import commands as c


class NanoKontrol2(Controller):
    SLIDERS = (0, 1, 2, 3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22, 23)

    def is_button(self, code):
        return code not in self.SLIDERS


def factory(*args, **kwargs):

    nk2 = NanoKontrol2(*args, **kwargs)
    nk2.event_manager.register_modifier(42, 'stopbtn')

    nk2.keyup(45, c.SWITCH)
    nk2.keyup(61, c.ifnotmod('stopbtn', c.LEFT)) 
    nk2.keyup(62, c.ifnotmod('stopbtn', c.RIGHT)) 
    nk2.keyup(32, c.TOGGLE_V1) 
    nk2.keyup(33, c.TOGGLE_V2) 
    nk2.keyup(34, c.TOGGLE_A1) 
    nk2.keyup(35, c.TOGGLE_A2) 
    nk2.keyup(36, c.TOGGLE_A3) 
    nk2.keyup(37, c.TOGGLE_A4) 
    nk2.keyup(38, c.TOGGLE_A5) 
    nk2.keyup(39, c.TOGGLE_A6) 
    nk2.keyup(41, c.ifmod(
        'stopbtn', [c.JOG, c.addmodifier(nk2, 'scrub')],
        c.PLAY))
    nk2.keyup(42, c.remmodifier(nk2, 'scrub'))

    nk2.longpress(41, c.cmd(c.PREVIEW, stop=True))
    nk2.longpress(42, c.TILE_TO_VIEWER, c.cmd(
        c.remmodifier(nk2, 'scrub'), stop=False))
    nk2.longpress(45, c.FULLSCREEN_TOGGLE)
    nk2.longpress(32, c.DISABLE_ALL_TRACKS, c.TOGGLE_V1)
    nk2.longpress(33, c.DISABLE_ALL_TRACKS, c.TOGGLE_V2)
    nk2.longpress(34, c.DISABLE_ALL_TRACKS, c.TOGGLE_A1)
    nk2.longpress(35, c.DISABLE_ALL_TRACKS, c.TOGGLE_A2)
    nk2.longpress(36, c.DISABLE_ALL_TRACKS, c.TOGGLE_A3)
    nk2.longpress(37, c.DISABLE_ALL_TRACKS, c.TOGGLE_A4)
    nk2.longpress(38, c.DISABLE_ALL_TRACKS, c.TOGGLE_A5)
    nk2.longpress(39, c.DISABLE_ALL_TRACKS, c.TOGGLE_A6)
    nk2.longpress(60, c.MARK_CLIP)
    nk2.longpress(61, c.HOME)
    nk2.longpress(62, c.END)
    nk2.longpress(71, c.CLOSE_ALL_GAPS)

    nk2.keydown(42, c.STOP)
    nk2.keydown(43, c.ifmod('stopbtn', c.REVERSE_NUDGE, 'key j'))
    nk2.keydown(44, c.ifmod('stopbtn', c.FORWARD_NUDGE, 'key l'))
    nk2.keydown(46, c.JOIN)
    nk2.keydown(51, c.BIN_NEXT)
    nk2.keydown(52, c.INSERT)
    nk2.keydown(53, c.REPLACE)
    nk2.keydown(54, c.EMPTY_CUT)
    nk2.keydown(55, c.ifmod('stopbtn', c.INSERT))
    nk2.keydown(58, c.ifmod('stopbtn', c.UNDO, c.MARK_IN))
    nk2.keydown(59, c.ifmod('stopbtn', c.REDO, c.MARK_OUT))
    nk2.keydown(60, c.ifmod('stopbtn', c.UNMARK, c.MARK_IN))
    nk2.keydown(61, c.ifmod('stopbtn', c.MARK_IN))
    nk2.keydown(62, c.ifmod('stopbtn', c.MARK_OUT))
    nk2.keydown(70, c.REMOVE)
    nk2.keydown(71, c.DELETE)

    nk2.slidedown(16, c.ifmod('stopbtn', c.scrub_left))
    nk2.slideup(16, c.ifmod('stopbtn', c.scrub_right))
    nk2.slidedown(17, c.ifmod('stopbtn', c.frames_left))
    nk2.slideup(17, c.ifmod('stopbtn', c.frames_right))
    nk2.slidedown(18, c.ifmod('stopbtn', c.command(threshold=0.25)(c.cmd(c.BIN_PREV))))
    nk2.slideup(18, c.ifmod('stopbtn', c.command(threshold=0.25)(c.cmd(c.BIN_NEXT))))
    nk2.slidedown(23, c.knob(c.zoom_in))
    nk2.slideup(23, c.knob(c.zoom_out))
    nk2.slidedown(7, c.ifmod('stopbtn', c.slider(c.zoom_in)))
    nk2.slideup(7, c.ifmod('stopbtn', c.slider(c.zoom_out)))

    nk2.doublehit(
            42, c.GOTO_MARK_IN, c.TILE_TO_VIEWER,
            c.remmodifier(nk2, 'scrub'))
    return nk2
