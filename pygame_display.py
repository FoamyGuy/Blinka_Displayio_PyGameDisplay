# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Tim C for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`foamyguy_blinka_displayio_pygamedisplay`
================================================================================

Use CircuitPython displayio code on PC and Raspberry Pi outputting to a PyGame window instead of a phyisical display.


* Author(s): Tim C

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/foamyguy/Foamyguy_CircuitPython_Blinka_Displayio_PyGameDisplay.git"

import time

import displayio
import pygame
from PIL import Image
from recordclass import recordclass

_INIT_SEQUENCE = None

Rectangle = recordclass("Rectangle", "x1 y1 x2 y2")


# pylint: disable=too-few-public-methods
class PyGameDisplay(displayio.Display):
    """PyGame display driver"""

    def __init__(self,  **kwargs):
        self.running = True
        super().__init__(None, _INIT_SEQUENCE, **kwargs)


    def _initialize(self, init_sequence):
        # initialize the pygame module
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("blinka.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Blinka Displayio PyGame")

        self._pygame_screen = pygame.display.set_mode((self._width, self._height))

    def _write(self, command, data):
        pass
        # don't need to write to anything

    def _release(self):
        pass
        # maybe quit pygame?

    def refresh(self, *, target_frames_per_second=60, minimum_frames_per_second=1):
        """When auto refresh is off, waits for the target frame rate and then refreshes the
        display, returning True. If the call has taken too long since the last refresh call
        for the given target frame rate, then the refresh returns False immediately without
        updating the screen to hopefully help getting caught up.

        If the time since the last successful refresh is below the minimum frame rate, then
        an exception will be raised. Set minimum_frames_per_second to 0 to disable.

        When auto refresh is on, updates the display immediately. (The display will also
        update without calls to this.)
        """
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                self.running = False
                time.sleep(0.05)
                pygame.quit()

        if self.running:
            self._subrectangles = []

            # Go through groups and and add each to buffer
            if self._current_group is not None:
                buffer = Image.new("RGBA", (self._width, self._height))
                # Recursively have everything draw to the image
                self._current_group._fill_area(buffer)  # pylint: disable=protected-access
                # save image to buffer (or probably refresh buffer so we can compare)
                self._buffer.paste(buffer)

            if self._current_group is not None:
                # Eventually calculate dirty rectangles here
                self._subrectangles.append(Rectangle(0, 0, self._width, self._height))

            for area in self._subrectangles:
                self._refresh_display_area(area)

    def _refresh_display_area(self, rectangle):
        """Loop through dirty rectangles and redraw that area."""

        img = self._buffer.convert("RGB").crop(rectangle)
        img = img.rotate(self._rotation, expand=True)

        display_rectangle = self._apply_rotation(rectangle)
        img = img.crop(self._clip(display_rectangle))

        raw_str = img.tobytes("raw", 'RGB')
        pygame_surface = pygame.image.fromstring(raw_str, (img.width, img.height), 'RGB')
        self._pygame_screen.blit(pygame_surface, (rectangle.x1, rectangle.y1))
        pygame.display.flip()
