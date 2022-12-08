# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2020 Tim C for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`blinka_displayio_pygamedisplay`
================================================================================

Use CircuitPython displayio code on PC and Raspberry Pi output to a
PyGame window instead of a physical display.

* Author(s): Tim C

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/foamyguy/Foamyguy_CircuitPython_Blinka_Displayio_PyGameDisplay.git"

import time
from dataclasses import astuple

import displayio
import pygame
from PIL import Image, ImageDraw
from displayio._structs import RectangleStruct
from recordclass import recordclass

_INIT_SEQUENCE = None

Rectangle = recordclass("Rectangle", "x1 y1 x2 y2")


# pylint: disable=too-few-public-methods
class PyGameDisplay(displayio.Display):
    """PyGame display driver

    Represents one PyGame window. Uses None for all display
    hardware parameters.
    """

    def __init__(self, icon=None, **kwargs):
        """
        icon - optional icon for the PyGame window
        """
        self._running = True
        self._icon = None
        if icon:
            self._icon = icon
        self._subrectangles = []
        self._pygame_screen = None
        super().__init__(None, _INIT_SEQUENCE, **kwargs)

    def _initialize(self, init_sequence):
        # pylint: disable=unused-argument
        # initialize the pygame module
        pygame.init()  # pylint: disable=no-member
        # load and set the logo

        if self._icon:
            print(f"loading icon: {self._icon}")
            icon = pygame.image.load(self._icon)
            pygame.display.set_icon(icon)

        pygame.display.set_caption("Blinka Displayio PyGame")

        self._pygame_screen = pygame.display.set_mode((self._width, self._height))

    def _write(self, command, data):
        pass
        # don't need to write to anything

    def _release(self):
        pass
        # maybe quit pygame?

    def refresh(self, *, target_frames_per_second=60, minimum_frames_per_second=1):
        """
        When auto refresh is off, waits for the target frame rate and then refreshes the
        display, returning True. If the call has taken too long since the last refresh call
        for the given target frame rate, then the refresh returns False immediately without
        updating the screen to hopefully help getting caught up.

        If the time since the last successful refresh is below the minimum frame rate, then
        an exception will be raised. Set minimum_frames_per_second to 0 to disable.

        When auto refresh is on, updates the display immediately. (The display will also
        update without calls to this.)

        """

        # pylint: disable=no-member, unused-argument, protected-access
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                self.running = False
                time.sleep(0.1)
                pygame.quit()

        if self._running:
            self._subrectangles = []
            force_full_refresh = False

            # Go through groups and and add each to buffer
            if self._core._current_group is not None:

                buffer = Image.new("RGBA", (self._core._width, self._core._height))
                # Recursively have everything draw to the image

                self._core._current_group._fill_area(
                    buffer
                )  # pylint: disable=protected-access
                # save image to buffer (or probably refresh buffer so we can compare)
                self._buffer.paste(buffer)
            else:
                # show nothing
                buffer = Image.new("RGBA", (self._core._width, self._core._height))
                draw = ImageDraw.Draw(buffer)
                draw.rectangle([(0, 0), buffer.size], fill=(0, 0, 0))
                self._buffer.paste(buffer)
                force_full_refresh = True

            if (force_full_refresh):
                full_rect = RectangleStruct(0, 0, self._width, self._height)
                self._refresh_display_area(full_rect)
            else:
                self._subrectangles = self._core.get_refresh_areas()
                print(self._subrectangles)
                for area in self._subrectangles:
                    self._refresh_display_area(area)

    def _refresh_display_area(self, rectangle):
        """Loop through dirty rectangles and redraw that area."""

        img = self._buffer.convert("RGB").crop(astuple(rectangle))
        img = img.rotate(self._rotation, expand=True)
        display_rectangle = self._apply_rotation(rectangle)
        img = img.crop(astuple(self._clip(display_rectangle)))
        raw_str = img.tobytes("raw", "RGB")
        pygame_surface = pygame.image.fromstring(
            raw_str, (img.width, img.height), "RGB"
        )
        # print("({}, {})".format(img.width, img.height))
        self._pygame_screen.blit(pygame_surface, (rectangle.x1, rectangle.y1))
        pygame.display.flip()

    @property
    def running(self):
        """
        True when the display is running. False means that the user has clicked the
        exit button in top right corner of the window.

        This method will call refresh() if auto_refresh is True. This allows the
        auto_refresh functionality to work without threading.
        """
        if self.auto_refresh:
            self.refresh()
        return self._running

    @running.setter
    def running(self, new_running_val):
        self._running = new_running_val

    @property
    def auto_refresh(self) -> bool:
        """True when the display is refreshed automatically."""
        return self._auto_refresh

    @auto_refresh.setter
    def auto_refresh(self, value: bool):
        self._auto_refresh = value
