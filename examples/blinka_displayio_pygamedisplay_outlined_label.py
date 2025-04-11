# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Make green and purple rectangles and a
"Hello World" label.
"""

from blinka_displayio_pygamedisplay import PyGameDisplay

from adafruit_display_text import outlined_label
import terminalio
import displayio

# Make the display context. Change size if you want
display = PyGameDisplay(width=320, height=240, auto_refresh=False)

text_area = outlined_label.OutlinedLabel(
    terminalio.FONT,
    text="Outlined\nLabel",
    color=0xFF00FF,
    outline_color=0x00FF00,
    outline_size=1,
    scale=5,
)
text_area.anchor_point = (0, 0)
text_area.anchored_position = (20, 10)


# Make the display context
main_group = displayio.Group()
display.root_group = main_group

main_group.append(text_area)

display.refresh()
while True:
    if display.check_quit():
        break
