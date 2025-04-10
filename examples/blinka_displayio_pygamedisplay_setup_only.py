# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Make green and purple rectangles and a
"Hello World" label.
"""

from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio

# Make the display context. Change size if you want
display = PyGameDisplay(width=320, height=240, auto_refresh=False)

# Make the display context
main_group = displayio.Group()
display.root_group = main_group


display.refresh()
while True:
    if display.check_quit():
        break
