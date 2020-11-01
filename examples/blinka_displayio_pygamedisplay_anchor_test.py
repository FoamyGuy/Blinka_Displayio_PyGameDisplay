# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Testing anchor point of adafruit_display_text label.
"""
import terminalio
import displayio
from adafruit_display_text import label
from blinka_pygame_display import PyGameDisplay

display = PyGameDisplay(width=1770, height=920)

text_area = label.Label(terminalio.FONT, text="Hello world", scale=3)

text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (display.width // 2, display.height // 2)
print(text_area.bounding_box)
print(f"{text_area.x}, {text_area.y}")
main_group = displayio.Group()
main_group.append(text_area)
display.show(main_group)

# text_area.y = 37
while display.running:
    pass
