# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
example showing the use of adafruit_progressbar
"""
# pip install adafruit-circuitpython-progressbar
import time
import displayio
from adafruit_progressbar.progressbar import ProgressBar
from blinka_displayio_pygamedisplay import PyGameDisplay

# Make the display context
# Remove scaling so child elements render at native size
splash = displayio.Group()

display = PyGameDisplay(width=480, height=320)

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x0000FF

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

display.root_group = splash

# set progress bar width and height relative to the display
# Keep margins so it fits nicely centered in the window
width = display.width - 80  # narrower to ensure it fits
height = 24

x = display.width // 2 - width // 2
y = display.height // 3

# Create a new progress_bar object at (x, y)
progress_bar = ProgressBar(x, y, width, height, 1.0)

# Append progress_bar to the splash group
splash.append(progress_bar)

current_progress = 0.0
display.refresh()
# Increment progress once to 100%, then exit
for current_progress in range(0, 101, 1):
    print("Progress: {}%".format(current_progress))
    progress_bar.progress = current_progress / 100  # convert to decimal
    display.refresh()
    # Allow window close during the run
    if display.check_quit(delay=0.0):
        break
    time.sleep(0.01)

# Briefly show 100% before quitting
time.sleep(0.2)
