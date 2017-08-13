# midicontrol

A prototype midi->keystrokes handler.
Tested with Korg Nanokontrol2.

The prototype includes initial mapping for Lightworks NLE.

## Requirements

```
pip install --user python-xlib rtmidi
```

## Usage

```
python -m midicontrol.main
```

Or with specifying a target window:

```
python -m midicontrol.main -w windowname
```
