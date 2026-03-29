import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.scanners import DiodeOrientation

#oled
OLED = False
try:
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_ssd1306

```
displayio.release_displays()
i2c = busio.I2C(board.GP7, board.GP6)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

splash = displayio.Group()
display.show(splash)

mode_text = label.Label(terminalio.FONT, text="Mode: MEDIA", x=0, y=10)
vol_text = label.Label(terminalio.FONT, text="Vol : █████░░░░░", x=0, y=30)
stat_text = label.Label(terminalio.FONT, text="Stat: ▶", x=0, y=50)

splash.append(mode_text)
splash.append(vol_text)
splash.append(stat_text)

OLED = True
```

except:
OLED = False

# state

current_mode = 0
volume_level = 5
is_playing = True

mode_names = ["MEDIA", "STUDY", "GAMING"]

def update_display():
if not OLED:
return

```
mode_text.text = "Mode: " + mode_names[current_mode]

bars = "█" * volume_level + "░" * (10 - volume_level)
vol_text.text = "Vol : " + bars

stat_text.text = "Stat: " + ("▶" if is_playing else "⏸")
```

#keyboard
keyboard = KMKKeyboard()
layers = Layers()
keyboard.modules.append(layers)

keyboard.row_pins = (board.GP26, board.GP27, board.GP28)
keyboard.col_pins = (board.GP29, board.GP6, board.GP7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

#custom keys

from kmk.keys import make_key

def mode_handler(key, keyboard, *args):
global current_mode
current_mode = (current_mode + 1) % 3
keyboard.active_layers = [current_mode]
update_display()

def vol_up_handler(key, keyboard, *args):
global volume_level
if volume_level < 10:
volume_level += 1
update_display()

def vol_down_handler(key, keyboard, *args):
global volume_level
if volume_level > 0:
volume_level -= 1
update_display()

def play_handler(key, keyboard, *args):
global is_playing
is_playing = not is_playing
update_display()

MODE = make_key(names=('MODE',), on_press=mode_handler)
VOLUP = make_key(names=('VOLUP',), on_press=vol_up_handler)
VOLDN = make_key(names=('VOLDN',), on_press=vol_down_handler)
PLAY = make_key(names=('PLAY',), on_press=play_handler)

#keymap

keyboard.keymap = [

```
# MEDIA MODE
[
    KC.MUTE, VOLUP, VOLDN,
    PLAY, KC.MNXT, KC.MPRV,
    MODE, KC.COPY, KC.PASTE
],

# STUDY MODE
[
    KC.UNDO, KC.REDO, KC.S,
    KC.F, KC.COPY, KC.PASTE,
    MODE, KC.TAB, KC.ENTER
],

# GAMING MODE
[
    KC.N1, KC.N2, KC.N3,
    KC.Q, KC.W, KC.E,
    MODE, KC.SPC, KC.ESC
]
```

]

update_display()

if **name** == '**main**':
keyboard.go()
