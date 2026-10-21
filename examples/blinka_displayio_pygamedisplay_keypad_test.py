# SPDX-FileCopyrightText: 2020 Tim C
#
# SPDX-License-Identifier: Unlicense
"""
Testing keypad-processing
"""

import displayio
import terminalio
import time

import pygame

from adafruit_display_text import label
from blinka_displayio_pygamedisplay import PyGameDisplay

# set to True to catch all keys
ALL_KEYS = False

# create display
display = PyGameDisplay(
    width=400,
    height=300,
    native_frames_per_second=60,
)

# create keypad
if ALL_KEYS:
    kp_keys = []
    kp_text = "press any key"
else:
    kp_keys = [pygame.K_LEFT, pygame.K_HOME, pygame.K_RIGHT]
    kp_text = "available keys: left, home, right"
kp = display.keypad(kp_keys, value_when_pressed=True, interval=0.02)

# create and center text area
text_area = label.Label(terminalio.FONT, text=kp_text, scale=1)
text_area.anchor_point = (0.5, 0.5)
text_area.anchored_position = (display.width // 2, display.height // 2)

main_group = displayio.Group()
main_group.append(text_area)
display.root_group = main_group
display.refresh()

# This loop will wait for key presses and update the display.
# Note that this is not a really useful example, since compound keys
# will trigger multiple events and the application must handle this
# individually.

last_event = 0
while True:
    if display.check_quit():
        break
    while True:
        event = kp.events.get()  # a keypad-event, not a pygame-event!
        if event and event.pressed:
            if text_area.text == kp_text:  # remove prompt
                text_area.text = ""
            # append key to output
            text_area.text += pygame.key.name(
                kp_keys[event.key_number] if kp_keys else event.key_number,
                use_compat=True,
            )
            last_event = time.monotonic()
        else:
            break
    if time.monotonic() - last_event > 5:
        # reset prompt
        text_area.text = kp_text
