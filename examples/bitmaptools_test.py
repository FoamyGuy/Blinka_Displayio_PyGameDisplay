# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Make green and purple rectangles and a
"Hello World" label.
"""
import math

from blinka_displayio_pygamedisplay import PyGameDisplay
import bitmaptools
import displayio
import numpy as np

# Make the display context. Change size if you want
display = PyGameDisplay(width=320, height=240, auto_refresh=False)
print(display.width, display.height)
# Make the display context
main_group = displayio.Group(scale=16)
display.root_group = main_group

bmp = displayio.Bitmap(320//4, 240//4, 16)
palette = displayio.Palette(16)
palette[0] = 0x000000
palette[1] = 0xffffff
palette[2] = 0xff0000
palette[3] = 0x00ff00
palette[4] = 0x0000ff
palette[5] = 0xffff00
palette[6] = 0x00ffff
palette[7] = 0xff00ff

bmp.fill(3)

tg = displayio.TileGrid(bmp, pixel_shader=palette)
main_group.append(tg)


#bitmaptools.fill_region(bmp, display.width - 40, display.height-40, display.width, display.height, 4)
#bitmaptools.draw_line(bmp, 0,0, display.width, display.height, 4)
#bitmaptools.draw_circle(bmp, 80, 80, 60, 4)

# xs = bytes([4, 101, 101, 19])
# ys = bytes([4, 19,  121, 101])
# bitmaptools.draw_polygon(bmp, xs, ys, 4)
#
# xs = bytes([14, 60, 110])
# ys = bytes([14, 24,  90])
# bitmaptools.draw_polygon(bmp, xs, ys, 2, close=True)

# bitmaptools.blit(bmp, bmp, 120, 120,
#                  x1=0, y1=0, x2=80, y2=80,
#                  skip_source_index=2,
#                  skip_dest_index=3)

# bitmaptools.rotozoom(
#     bmp, bmp, ox=bmp.width//2+100, oy=bmp.height//2+ 100,
#     dest_clip0=(0,0), dest_clip1=(bmp.width, bmp.height),
#     px=0, py=0,
#     source_clip0=(0,0), source_clip1=(120, 130),
#     angle=math.radians(210), scale=1.0, skip_index=None
# )

#bitmaptools.draw_line(bmp, x1=110,y1=90, x2=130, y2=120, value=4)
#bitmaptools.draw_line(bmp, x1=60,y1=24, x2=110, y2=90, value=4)
rows = []
for y in range(bmp.height):
    for x in range(bmp.width):
        rows.extend([(y*bmp.width + x + y) % 8])


#print(rows)
array_2d = np.array(rows, dtype=np.uint8)
# print(array_2d)
# print(len(array_2d))
#bitmaptools.arrayblit(bmp, rows, skip_index=2)

with open("bin_img.bin", "rb") as f:
    bitmaptools.readinto(bmp, f, 8)

display.refresh()
while True:
    if display.check_quit():
        break
