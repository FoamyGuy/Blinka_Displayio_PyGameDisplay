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

# pylint: disable=protected-access

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/foamyguy/Foamyguy_CircuitPython_Blinka_Displayio_PyGameDisplay.git"

import time
import threading
from dataclasses import astuple
import displayio
import pygame
from PIL import Image
from recordclass import recordclass

_INIT_SEQUENCE = None

Rectangle = recordclass("Rectangle", "x1 y1 x2 y2")


# pylint: disable=too-few-public-methods
class PyGameDisplay(displayio.Display):
    """PyGame display driver

    Represents one PyGame window. Uses None for all display
    hardware parameters.
    """

    def __init__(
        self,
        width=0,
        height=0,
        icon=None,
        native_frames_per_second=60,
        flags=0,
        **kwargs,
    ):
        # pylint: disable=too-many-arguments
        """
        width  - width of the display. A value of zero maximizes the display
        height - height of the display. A value of zero maximizes the display
        icon - optional icon for the PyGame window
        native_frames_per_second - high values result in high cpu-load
        flags - pygame display-flags, e.g. pygame.FULLSCREEN or pygame.NOFRAME
        """
        self._native_frames_per_second = native_frames_per_second
        self._icon = None
        if icon:
            self._icon = icon
        self._flags = flags
        self._subrectangles = []

        self._pygame_screen = None
        self._pygame_display_thread = None
        self._pygame_display_tevent = threading.Event()
        self._pygame_display_force_update = False

        if (flags & pygame.FULLSCREEN) or width == 0 or height == 0:
            width, height = self._get_screen_size()

        super().__init__(None, _INIT_SEQUENCE, width=width, height=height, **kwargs)

    def _get_screen_size(self):
        """autodetect screen-size: returns tuple (width,height)"""

        # a bit clumsy: we need to init and deinit pygame for this
        pygame.init()  # pylint: disable=no-member
        width = pygame.display.get_desktop_sizes()[0][0]
        height = pygame.display.get_desktop_sizes()[0][1]
        pygame.quit()
        return width, height

    def _initialize(self, init_sequence):
        # pylint: disable=unused-argument
        # just start the pygame-refresh loop
        self._pygame_display_thread = threading.Thread(
            target=self._pygame_refresh, daemon=True
        )
        self._pygame_display_thread.start()

    def _pygame_refresh(self):
        # initialize the pygame module
        pygame.init()  # pylint: disable=no-member
        # load and set the logo

        if self._icon:
            print(f"loading icon: {self._icon}")
            icon = pygame.image.load(self._icon)
            pygame.display.set_icon(icon)

        pygame.display.set_caption("Blinka Displayio PyGame")

        self._pygame_screen = pygame.display.set_mode(
            size=(self._width, self._height), flags=self._flags
        )

        # pygame-refresh loop
        while not self._pygame_display_tevent.is_set():
            time.sleep(1 / self._native_frames_per_second)
            # refresh pygame-display
            if not self._auto_refresh and not self._pygame_display_force_update:
                pygame.display.flip()
                continue

            self._pygame_display_force_update = False

            # Go through groups and and add each to buffer
            if self._core._current_group is not None:
                buffer = Image.new("RGBA", (self._core._width, self._core._height))
                # Recursively have everything draw to the image

                self._core._current_group._fill_area(
                    buffer
                )  # pylint: disable=protected-access
                # save image to buffer (or probably refresh buffer so we can compare)
                self._buffer.paste(buffer)

            self._subrectangles = self._core.get_refresh_areas()
            for area in self._subrectangles:
                self._refresh_display_area(area)

    def _write(self, command, data):
        pass
        # don't need to write to anything

    def _release(self):
        self._pygame_display_tevent.set()
        self._pygame_display_thread.join()
        pygame.quit()

    def refresh(self, *, target_frames_per_second=60, minimum_frames_per_second=1):
        """
        While normal display-objects call this method also within a refresh
        loop, this implementation uses this method only for explicit updates.
        Note that we cannot just call the update-logic directly, since
        the pygame-display was created on another thread.
        """
        # pylint: disable=no-member, unused-argument, protected-access
        if not self._auto_refresh:
            self._pygame_display_force_update = True

    def check_quit(self):
        """
        Check if the quit button on the window is being pressed.
        """
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # stop and leave method
                    self._pygame_display_tevent.set()
                    self._pygame_display_thread.join()
                    pygame.quit()
                    return True
        except pygame.error:
            return True
        return False

    def event_loop(self, interval=None, on_time=None, on_event=None, events=None):
        """
        pygame event-loop. Has to be called by the main thread. This method
        terminates in case of a QUIT-event. An optional callback on_time is
        executed every interval seconds. Use this callback for
        application specific logic.
        """
        if events is None:
            events = []
        if interval is None:
            interval = -1
        next_time = time.monotonic() + interval
        while True:
            for event in pygame.event.get():
                # pylint: disable=no-else-return
                if event.type == pygame.QUIT:
                    # stop and leave method
                    self._pygame_display_tevent.set()
                    self._pygame_display_thread.join()
                    pygame.quit()
                    return
                elif event.type in events:
                    # use callback for event-processing
                    on_event(event)
            # execute application logic
            if on_time and time.monotonic() > next_time:
                on_time()
                next_time = time.monotonic() + interval

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
    def auto_refresh(self) -> bool:
        """True when the display is refreshed automatically."""
        return self._auto_refresh

    @auto_refresh.setter
    def auto_refresh(self, value: bool):
        self._auto_refresh = value
