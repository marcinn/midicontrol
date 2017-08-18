import pkg_resources
import configparser


class KeyboardAlreadyRegistered(Exception):
    pass


class KeyboardsRegistry(object):
    def __init__(self):
        self._items = {}

    def register(self, keyboard):
        key = keyboard.product_id

        if key in self._items:
            raise KeyboardAlreadyRegistered(key)

        self._items[key] = keyboard

    def get(self, product_id):
        return self._items[product_id]

    def items(self):
        return self._items.items()


registry = KeyboardsRegistry()


class MidiKeyboard(object):
    def __init__(
            self, product_id, midi_port_name, name=None, sliders=None,
            knobs=None, meta=None):
        self.product_id = product_id
        self.midi_port_name = midi_port_name
        self.name = name
        self.sliders = sliders or []
        self.knobs = knobs or []
        self.meta = meta or {}

    def __str__(self):
        return self.name or self.product_id

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, meta):
        self._meta = dict(zip(
            meta.keys(), map(int, meta.values())))
        self._meta_rev = dict(map(
            lambda x: (x[1], x[0]), self._meta.items()))

    @property
    def sliders(self):
        return self._sliders

    @sliders.setter
    def sliders(self, sliders):
        self._sliders = list(map(int, sliders))

    @property
    def knobs(self):
        return self._knobs

    @knobs.setter
    def knobs(self, knobs):
        self._knobs = list(map(int, knobs))

    def is_slider(self, code):
        return code in self.sliders

    def is_knob(self, code):
        return code in self.knobs

    def is_button(self, code):
        return not self.is_slider(code) and not self.is_knob(code)

    def meta_to_code(self, meta):
        return self._meta[meta]

    def code_to_meta(self, code):
        return self._meta_rev[code]


def create_midikeyboard(config):
    device = config['Device']
    meta = dict(config.items('Meta') or [])
    controls = dict(config.items('Controls') or [])

    return MidiKeyboard(
            product_id=device['productid'],
            midi_port_name=device['midiportname'],
            name=device.get('name'),
            sliders=controls.get('sliders', '').split(','),
            knobs=controls.get('knobs', '').split(','),
            meta=meta)


def load_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def initialize():
    resources = pkg_resources.resource_listdir(
                    'midicontrol', 'data/devices')
    for resource in resources:
        config = load_config(
            pkg_resources.resource_filename(
                'midicontrol', 'data/devices/%s' % resource))
        registry.register(create_midikeyboard(config))
