import rtmidi
import traceback
import argparse
import time

from .controller import Controller
from . import keyboards


def safe_handle(callback):
    def wrapped(*args, **kw):
        try:
            callback(*args, **kw)
        except Exception:
            traceback.print_exc()
    return wrapped


def main(controller):
    midi_port_name = controller.keyboard.midi_port_name
    port = rtmidi.RtMidiIn()

    tries = 0
    port_number = None

    while tries < 10:
        for x in range(port.getPortCount()):
            if port.getPortName(x).startswith(midi_port_name):
                port_number = x
                break
        if port_number is None:
            print("Waiting for device: %s" % midi_port_name)
            time.sleep(1)
            tries += 1
        else:
            break

    if port_number is None:
        raise ValueError(
                'Midi port "%s" was not found' % midi_port_name)

    port.openPort(port_number)
    port.setCallback(safe_handle(controller.handle_midi_event))

    print("Ctrl-C to abort")

    controller.run()
    port.closePort()


def list_keyboards(opts):
    for id_, keyboard in keyboards.registry.items():
        print("{0} {1} ({2})".format(
            keyboard.name, type(keyboard).__name__,
            keyboard.product_id))


def start(opts):
    try:
        product_id = opts.keyboard.split('_')[0]
    except IndexError:
        product_id = opts.keyboard

    try:
        keyboard = keyboards.registry.get(product_id)
    except KeyError:
        print("Unhandled keyboard: %s" % product_id)
    else:
        print("Using device: {0}".format(keyboard))
        controller = Controller(
            keyboard=keyboard,
            target_window_name=opts.target_window_name)
        main(controller)


def run_cli():
    actions = {
            'start': start,
            'list-keyboards': list_keyboards,
            }

    keyboards.initialize()

    parser = argparse.ArgumentParser('Midi control to keyboard mapper')
    commands = parser.add_subparsers(help='List of possible commands', dest='action')

    start_parser = commands.add_parser('start')
    list_keyboards_parser = commands.add_parser('list-keyboards')

    start_parser.add_argument(
            '-d', dest='keyboard', action='store', required=True,
            help='Device identifier in format idVendor:idProduct (i.e. 0944:0117)')
    start_parser.add_argument(
            '-w', dest='target_window_name', action='store',
            help='send keys only to the window of matching name')

    opts = parser.parse_args()

    if opts.action:
        actions[opts.action](opts)
    else:
        parser.print_help()


if __name__ == '__main__':
    run_cli()
