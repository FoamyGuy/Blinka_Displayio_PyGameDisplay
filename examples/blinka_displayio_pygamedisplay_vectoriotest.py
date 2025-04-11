# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Make green and purple rectangles and a
"Hello World" label.
"""

import time
from blinka_displayio_pygamedisplay import PyGameDisplay
import displayio
import vectorio


# Make the display context
display = PyGameDisplay(icon="blinka.png", width=400, height=300)
display.rotation = 0
# Make the display context
main_group = displayio.Group()
display.root_group = main_group

color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFF00  # Bright Green

other_color_palette = displayio.Palette(1)
other_color_palette[0] = 0x00FF00  # Bright Green

circle = vectorio.Circle(pixel_shader=color_palette, radius=25, x=50, y=50)
main_group.append(circle)

rectangle = vectorio.Rectangle(
    pixel_shader=other_color_palette, width=40, height=30, x=155, y=145
)
main_group.append(rectangle)

points = [(5, 5), (100, 20), (20, 20), (20, 100)]
polygon = vectorio.Polygon(pixel_shader=color_palette, points=points, x=0, y=0)
main_group.append(polygon)

display.refresh()
while True:
    time.sleep(0.05)

    if display.check_quit():
        print("check_quit() was true")
        break
