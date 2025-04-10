# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Make green and purple rectangles and a
"Hello World" label.
"""

from blinka_displayio_pygamedisplay import PyGameDisplay
from adafruit_display_text.scrolling_label import ScrollingLabel
import terminalio
import displayio


# Make the display context. Change size if you want
display = PyGameDisplay(width=320, height=240, auto_refresh=False)

# Make the display context
main_group = displayio.Group()
display.root_group = main_group


text = "Hello world CircuitPython scrolling label"
my_scrolling_label = ScrollingLabel(
    terminalio.FONT, text=text, max_characters=20, animate_time=0.1, scale=2
)
my_scrolling_label.anchor_point = (0,0)
my_scrolling_label.anchored_position = (30, 30)


main_group.append(my_scrolling_label)

display.refresh()
while True:
    updated = my_scrolling_label.update()
    if updated:
        display.refresh()
    
    if display.check_quit():
        break
