# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense

"""
This is adapted from an example in the shapes library to work with pygame display.
It shows how to draw various different shapes and place them on the screen.
"""

import displayio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
# from adafruit_display_shapes.triangle import Triangle
# from adafruit_display_shapes.line import Line
# from adafruit_display_shapes.polygon import Polygon
from blinka_displayio_pygamedisplay import PyGameDisplay

# Make the display context
splash = displayio.Group(scale=2)

display = PyGameDisplay(icon="blinka.png", width=640, height=480)
display.root_group = splash

# Make a background color fill
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
bg_sprite = displayio.TileGrid(color_bitmap, x=0, y=0, pixel_shader=color_palette)
splash.append(bg_sprite)
##########################################################################

# splash.append(Line(220, 130, 270, 210, 0xFF0000))
# splash.append(Line(270, 210, 220, 210, 0xFF0000))
# splash.append(Line(220, 210, 270, 130, 0xFF0000))
# splash.append(Line(270, 130, 220, 130, 0xFF0000))
#
# # Draw a blue star
# polygon = Polygon(
#     [
#         (255, 40),
#         (262, 62),
#         (285, 62),
#         (265, 76),
#         (275, 100),
#         (255, 84),
#         (235, 100),
#         (245, 76),
#         (225, 62),
#         (248, 62),
#     ],
#     outline=0x0000FF,
# )
# polygon.x += 150
# polygon.y += 50
# splash.append(polygon)
#
# triangle = Triangle(170, 50, 120, 140, 210, 160, fill=0x00FF00, outline=0xFF00FF)
# triangle.x += 240
# triangle.y += 180
# splash.append(triangle)

rect = Rect(80, 20, 41, 41, fill=0x0)
splash.append(rect)

circle = Circle(100, 30, 20, fill=0x00FF00, outline=0xFF00FF)
circle.x += 200
splash.append(circle)

print(circle.fill)

rect2 = Rect(50, 100, 61, 81, outline=0x0, stroke=3)
rect2.y += 10
splash.append(rect2)


roundrect = RoundRect(10, 10, 61, 81, 10, fill=0x0, outline=0xFF00FF, stroke=6)
roundrect.y += 270//2
splash.append(roundrect)

display.refresh()
while True:
    if display.check_quit():
        break
