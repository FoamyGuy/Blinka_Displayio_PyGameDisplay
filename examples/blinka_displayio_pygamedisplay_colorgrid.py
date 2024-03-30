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
from vectorio import Rectangle

SIZE = (10, 10)
pixels = []
for y_idx in range(SIZE[1]):
    for x_idx in range(SIZE[0]):
        pixels.append((x_idx, y_idx))

# Make the display context. Change size if you want
display = PyGameDisplay(width=320, height=240, auto_refresh=False)

# Make the display context
main_group = displayio.Group()
display.root_group = main_group

blue = displayio.Palette(1)
blue[0] = 0x0000ff
red = displayio.Palette(1)
red[0] = 0xff0000
green = displayio.Palette(1)
green[0] = 0x00ff00
yellow = displayio.Palette(1)
yellow[0] = 0xffff00

palette_map = {
    "0xff0000": red,
    "0x00ff00": green,
    "0xffff00": yellow,
    "0x0000ff": blue
}

f = open("input_out.txt", "r")
input_str = f.read()
f.close()

grid = []
y_size = 10
x_size = 10

print(f"size: x:{x_size}, y:{y_size}")
for _y in range(y_size):
    grid.append([-1 for _ in range(x_size)])
    # for _x in range(x_size):
    #     grid[_y].append(-1)

print(grid)

for row in input_str.split("\n"):
    loc_str = row.split(": ")[0]
    loc_str = loc_str.replace(")", "")
    loc_str = loc_str.replace("(", "")
    loc_str = loc_str.replace(" ", "")
    print(f"loc str: {loc_str}")

    hex_str = row.split(": ")[-1]

    x_cell = int(loc_str.split(",")[0])
    y_cell = int(loc_str.split(",")[1])
    grid[y_cell][x_cell] = hex_str
    x_loc = x_cell * 21
    y_loc = y_cell * 21
    print(f"{x_loc}, {y_loc}")
    rect = Rectangle(pixel_shader=palette_map[row.split(": ")[-1]],
                     x=x_loc, y=y_loc, width=20, height=20)
    main_group.append(rect)
    # time.sleep(0.05)

# display.auto_refresh = True
display.refresh()
time.sleep(0.05)
display.refresh()

print(grid)


def find_contiguous(grid, x, y) -> list:
    shape_cells = []

    target_color = grid[y][x]

    checking_queue = [(x, y)]
    seen = set()
    while checking_queue:
        loc = checking_queue.pop()
        if loc in seen:
            continue
        seen.add(loc)
        print(f"checking {loc}")
        if 0 <= loc[0] < len(grid[0]) and 0 <= loc[1] < len(grid):
            if grid[loc[1]][loc[0]] == target_color:
                shape_cells.append(loc)

                checking_queue.append((loc[0] + 1, loc[1]))
                checking_queue.append((loc[0] - 1, loc[1]))
                checking_queue.append((loc[0], loc[1] + 1))
                checking_queue.append((loc[0], loc[1] - 1))
    return shape_cells


# print(find_contiguous(grid, 1, 0))

scores = {}

seen = set()
for pixel in pixels:
    if pixel in seen:
        continue
    # seen.add(pixel)

    same_color_shape = find_contiguous(grid, pixel[0], pixel[1])

    for loc in same_color_shape:
        seen.add(loc)
    
    if len(same_color_shape) > 1:
        if grid[pixel[1]][pixel[0]] in scores:
            if len(same_color_shape) >= 5:
                scores[grid[pixel[1]][pixel[0]]] += len(same_color_shape) * len(same_color_shape) 
            else:
                scores[grid[pixel[1]][pixel[0]]] += len(same_color_shape)
        else:
            scores[grid[pixel[1]][pixel[0]]] = len(same_color_shape)

print(scores)
while True:
    time.sleep(0.05)
    if display.check_quit():
        break
