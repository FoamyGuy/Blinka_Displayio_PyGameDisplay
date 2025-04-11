# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Initialize the PyGame display and add a button to it.
React to click events on the button
"""
import displayio
import pygame
import terminalio
from adafruit_button import Button
from blinka_displayio_pygamedisplay import PyGameDisplay

# --| Button Config |-------------------------------------------------
BUTTON_X = 110
BUTTON_Y = 95
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_STYLE = Button.ROUNDRECT
BUTTON_FILL_COLOR = 0x00FFFF
BUTTON_OUTLINE_COLOR = 0xFF00FF
BUTTON_LABEL = "HELLO WORLD"
BUTTON_LABEL_COLOR = 0x000000
# --| Button Config |-------------------------------------------------

display = PyGameDisplay(width=320, height=240)
splash = displayio.Group()
display.root_group = splash

GREEN = 0x00FF00
BLUE = 0x0000FF
CUR_COLOR = GREEN

color_bitmap = displayio.Bitmap(display.width, display.height, 1)
color_palette = displayio.Palette(1)
color_palette[0] = CUR_COLOR  # Bright Green
print(color_palette[0])
# Make the button
button = Button(
    x=BUTTON_X,
    y=BUTTON_Y,
    width=BUTTON_WIDTH,
    height=BUTTON_HEIGHT,
    style=BUTTON_STYLE,
    fill_color=BUTTON_FILL_COLOR,
    outline_color=BUTTON_OUTLINE_COLOR,
    label="HELLO WORLD",
    label_font=terminalio.FONT,
    label_color=BUTTON_LABEL_COLOR,
)

button.width = 130

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

splash.append(button)

button.body.fill = 0x0000FF
# pylint: disable=no-member

# Must check display.running in the main loop!
display.refresh()
while True:
    # get mouse up  events
    ev = pygame.event.get(eventtype=pygame.MOUSEBUTTONUP)
    # proceed events
    for event in ev:
        pos = pygame.mouse.get_pos()
        print(pos)
        button.selected = False
        if button.contains(pos):
            if CUR_COLOR == GREEN:
                print("change to blue")
                color_palette[0] = BLUE
                CUR_COLOR = BLUE
            else:
                color_palette[0] = GREEN
                CUR_COLOR = GREEN
            display.refresh()
    # get mouse down  events
    ev = pygame.event.get(eventtype=pygame.MOUSEBUTTONDOWN)
    for event in ev:
        pos = pygame.mouse.get_pos()
        print(pos)
        if button.contains(pos):
            button.selected = True

    if display.check_quit():
        break
