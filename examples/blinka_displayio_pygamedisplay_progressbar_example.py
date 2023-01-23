# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
example showing the use of adafruit_progressbar
"""
import time
import displayio
from adafruit_progressbar.adafruit_progressbar import ProgressBar
from blinka_displayio_pygamedisplay import PyGameDisplay

# Make the display context
splash = displayio.Group(scale=2)

display = PyGameDisplay(width=480, height=320)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x0000FF

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

display.show(splash)

# set progress bar width and height relative to board's display
width = display.width - 40
height = 30

x = display.width // 2 - width // 2
y = display.height // 3

# Create a new progress_bar object at (x, y)
progress_bar = ProgressBar(x, y, width, height, 1.0)

# Append progress_bar to the splash group
splash.append(progress_bar)

current_progress = 0.0
while True:
    # range end is exclusive so we need to use 1 bigger than max number that we want
    for current_progress in range(0, 101, 1):
        print("Progress: {}%".format(current_progress))
        progress_bar.progress = current_progress / 100  # convert to decimal
        time.sleep(0.01)
    time.sleep(0.3)
    progress_bar.progress = 0.0
    time.sleep(0.3)

    if display.check_quit():
        break
