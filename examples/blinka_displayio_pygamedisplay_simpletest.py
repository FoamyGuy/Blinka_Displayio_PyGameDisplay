# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Make green and purple rectangles and a
"Hello World" label.
"""
import time

import displayio
import rainbowio
import terminalio
from adafruit_display_text import label
from blinka_displayio_pygamedisplay import PyGameDisplay


# Make the display context
display = PyGameDisplay(icon="blinka.png", width=400, height=300)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Draw a green background
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

splash.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(display.width - 40, display.height - 40, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0xAA0088  # Purple
inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=20, y=20)
splash.append(inner_sprite)

# Draw a label
text_group = displayio.Group()
text_area = label.Label(terminalio.FONT, text="Hello World!", color=0xFFFF00, scale=4)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (display.width // 2, display.height // 2)

# text_group.append(text_area)  # Subgroup for text scaling
splash.append(text_area)

color_num = 0
while True:
    text_area.color = rainbowio.colorwheel(color_num)
    color_num += 1
    if color_num > 255:
        color_num = 0
    print(time.monotonic())
    time.sleep(0.05)

    if display.check_quit():
        break
