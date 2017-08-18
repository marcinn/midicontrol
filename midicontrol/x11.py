import Xlib.display

display = Xlib.display.Display()
root = display.screen().root


current_window = None
current_window_id = None


NET_WM_NAME = display.intern_atom('_NET_WM_NAME')
WM_CLASS = display.intern_atom('WM_CLASS')
NET_ACTIVE_WINDOW = display.intern_atom('_NET_ACTIVE_WINDOW')


def get_focused_window_name():
    if current_window:
        return current_window.get_full_property(WM_CLASS, 0).value
    return ''


def is_window_in_focus(name):
    return name in get_focused_window_name()


def _check_current_window_id():
    try:
        return root.get_full_property(
                NET_ACTIVE_WINDOW, Xlib.X.AnyPropertyType).value[0]
    except Xlib.error.XError:
        return None

def update():
    global current_window_id, current_window
    window_id = _check_current_window_id()

    if current_window_id is None or not window_id == current_window_id:
        window = display.create_resource_object('window', window_id)
        window.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
        current_window = window
        current_window_id = window_id
        print("Current window: {0}".format(get_focused_window_name()))

    event = display.next_event()

