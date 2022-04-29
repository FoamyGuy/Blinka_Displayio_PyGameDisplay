# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Make green and purple rectangles and a
"Hello World" label.
"""
import displayio

from adafruit_bitmap_font import bitmap_font

from adafruit_display_text import bitmap_label, label
from blinka_displayio_pygamedisplay import PyGameDisplay

# Make the display context. Change size if you want
display = PyGameDisplay(width=320, height=240)

font = bitmap_font.load_font("font/forkawesome-36.pcf")
w, h, dx, dy = font.get_bounding_box()

glyphs = "".join(chr(0xF000 + i) for i in range(8))

group = displayio.Group()

label = bitmap_label.Label(
    font=font, text=glyphs, background_color=0x0000DD, background_tight=True
)
# label = label.Label(font=font, text=glyphs, background_color=0x0000DD, background_tight=True)

label.anchor_point = (0, 0)
label.anchored_position = (0, 20)

group.append(label)
display.show(group)


while display.running:
    pass
