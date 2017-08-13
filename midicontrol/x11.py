import Xlib.display

display = Xlib.display.Display()


def get_focused_window():
    window = display.get_input_focus().focus
    wmname = window.get_wm_name()
    wmclass = window.get_wm_class()
    if wmclass is None and wmname is None:
        window = window.query_tree().parent
        wmname = window.get_wm_name()
    return window.get_wm_class()[0]


def is_window_in_focus(name):
    return name in get_focused_window()
