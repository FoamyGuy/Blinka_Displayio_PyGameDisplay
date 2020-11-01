# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Use adafruit_imageload to show a bitmap on the screen
"""
import displayio
import adafruit_imageload
from blinka_displayio_pygamedisplay import PyGameDisplay

display = PyGameDisplay(width=800, height=600)

bitmap, palette = adafruit_imageload.load(
    "robot_friend.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group to hold the TileGrid
img_group = displayio.Group()

# Add the TileGrid to the Group
img_group.append(tile_grid)

# Add the Group to the Display
display.show(img_group)

# Loop forever so you can enjoy your image
while display.running:
    pass
