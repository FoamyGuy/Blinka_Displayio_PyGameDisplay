import displayio
from pygame_display import PyGameDisplay
import adafruit_imageload

display = PyGameDisplay(width=1770, height=920)

bitmap, palette = adafruit_imageload.load("purple.bmp",
                                          bitmap=displayio.Bitmap,
                                          palette=displayio.Palette)

# Create a TileGrid to hold the bitmap
tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

# Create a Group to hold the TileGrid
img_group = displayio.Group(scale=3)

# Add the TileGrid to the Group
img_group.append(tile_grid)

#main_group = displayio.Group()
#main_group.append(img_group)

# Add the Group to the Display
display.show(img_group)

# Loop forever so you can enjoy your image
while display.running:
    pass