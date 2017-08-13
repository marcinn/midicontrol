# midicontrol

A prototype midi->keystrokes handler.
Tested with Korg Nanokontrol2.

The prototype includes initial mapping for Lightworks NLE.

## Requirements

1. Python packages

```
pip install --user python-xlib rtmidi
```

2. System tools

- xte (https://linux.die.net/man/1/xte)

## Usage

Will send keystrokes to any focused window:
```
python -m midicontrol.main
```

Will send keystrokes to the specified target window (by it's part of wm class name):

```
python -m midicontrol.main -w windowname
```
