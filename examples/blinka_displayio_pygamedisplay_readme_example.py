# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Initialize the PyGame display and fill it with green
"""
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay

display = PyGameDisplay(width=320, height=240)
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

display.refresh()
while True:
    if display.check_quit():
        break
