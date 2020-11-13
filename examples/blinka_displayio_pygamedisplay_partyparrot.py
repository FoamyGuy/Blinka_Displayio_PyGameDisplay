# SPDX-FileCopyrightText: 2020 Tim C, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
Party parrot animation code adapted from:
https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/master/IoT_Party_Parrot

Thank you @BlitzCityDIY
"""
import time
import adafruit_imageload
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay

display = PyGameDisplay(width=320, height=320)

group = displayio.Group(max_size=20, scale=10)

#  get the spritesheet from here:
#  https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/master/IoT_Party_Parrot

#  load in party parrot bitmap
parrot_bit, parrot_pal = adafruit_imageload.load(
    "partyParrotsTweet.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette
)

parrot_grid = displayio.TileGrid(
    parrot_bit,
    pixel_shader=parrot_pal,
    width=1,
    height=1,
    tile_height=32,
    tile_width=32,
    default_tile=10,
    x=0,
    y=0,
)

group.append(parrot_grid)

display.show(group)

parrot = True  #  state to track if an animation is currently running
party = 0  #  time.monotonic() holder
p = 0  #  index for tilegrid
party_count = 0  #  count for animation cycles

while display.running:
    #  when a new tweet comes in...
    if parrot:
        #  every 0.1 seconds...
        if (party + 0.1) < time.monotonic():
            #  the party parrot animation cycles
            parrot_grid[0] = p
            #  p is the tilegrid index location
            p += 1
            party = time.monotonic()
            #  if an animation cycle ends
            if p > 9:
                #  index is reset
                p = 0
                #  animation cycle count is updated
                party_count += 1
                print("party parrot", party_count)
