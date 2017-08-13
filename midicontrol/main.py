import rtmidi
import traceback
import argparse


def safe_handle(callback):
    def wrapped(*args, **kw):
        try:
            callback(*args, **kw)
        except Exception:
            traceback.print_exc()
    return wrapped


def main(midi_port_name, controller):
    port = rtmidi.RtMidiIn()

    port_number = None
    for x in range(port.getPortCount()):
        if port.getPortName(x).startswith(midi_port_name):
            port_number = x
            break
    if port_number is None:
        raise ValueError(
                'Midi port "%s" was not found' % midi_port_name)

    port.openPort(port_number)
    port.setCallback(safe_handle(controller.handle_midi_event))

    print("Ctrl-C to abort")

    controller.run()
    port.closePort()


if __name__ == '__main__':
    from .nanokontrol2 import factory

    parser = argparse.ArgumentParser('Midi control to keyboard mapper')
    parser.add_argument(
            '-w', dest='target_window_name', action='store',
            help='send keys only to the window of matching name')

    opts = parser.parse_args()

    controller = factory(
            target_window_name=opts.target_window_name)
    main('nanoKONTROL2', controller)
