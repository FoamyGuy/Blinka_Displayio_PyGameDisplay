# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import terminalio
import displayio
from adafruit_display_text import label
from pygame_display import PyGameDisplay

display = PyGameDisplay(width=1770, height=920)

text = "Hello world"
text_area = label.Label(terminalio.FONT, text=text, scale=3)

text_area.anchor_point = (0.0, 0.0)
text_area.anchored_position = (0, 0)
print(text_area.bounding_box)
print(f"{text_area.x}, {text_area.y}")
main_group = displayio.Group()
main_group.append(text_area)
display.show(main_group)

#text_area.y = 37
while display.running:
    pass