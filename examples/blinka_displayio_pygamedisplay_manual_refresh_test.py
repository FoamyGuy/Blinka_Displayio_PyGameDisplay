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

# Make the display context. Change size if you want
display = PyGameDisplay(width=320, height=240, auto_refresh=False)
# time.sleep(0.1)
# Make the display context
main_group = displayio.Group()
display.root_group = main_group

# Draw a green background
color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

main_group.append(bg_sprite)

display.refresh()
#time.sleep(0.1)
# display.refresh()
# 
color_palette[0] = 0xFFFF00
display.refresh()

while True:
    if display.check_quit():
        break
