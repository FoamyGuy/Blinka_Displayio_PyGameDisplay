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

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/foamyguy/Foamyguy_CircuitPython_Blinka_Displayio_PyGameDisplay.git"



print("before import pygame")
import pygame
print("after import pygame")

import numpy as np
import time
import threading
from dataclasses import astuple
import traceback

print("before import displayio")
import displayio

print("after import displayio")
from displayio._area import Area

_INIT_SEQUENCE = tuple()

print("hello?")




# pylint: disable=too-few-public-methods,too-many-instance-attributes
class PyGameDisplay():
    """PyGame display driver

    Represents one PyGame window. Uses None for all display
    hardware parameters.
    """

    def __init__(
            self,
            width=0,
            height=0,
            icon=None,
            caption="Blinka Displayio PyGame",
            native_frames_per_second=60,
            flags=0,
            **kwargs,
    ):
        # pylint: disable=too-many-arguments
        """
        width  - width of the window. A value of zero maximizes the window
        height - height of the window. A value of zero maximizes the window
        icon - optional icon for the PyGame window
        caption - caption for the PyGame window
        native_frames_per_second - high values result in high cpu-load
        flags - pygame display-flags, e.g. pygame.FULLSCREEN or pygame.NOFRAME
        """
        self._native_frames_per_second = native_frames_per_second
        self._icon = icon
        self._caption = caption
        self._flags = flags
        self._subrectangles = []

        self._pygame_screen = None
        self._pygame_display_thread = None
        self._pygame_display_tevent = threading.Event()
        self._pygame_display_force_update = False

        if (flags & pygame.FULLSCREEN) or width == 0 or height == 0:
            width, height = self._get_screen_size()

        print("before super init")
        super().__init__(None, _INIT_SEQUENCE, width=width, height=height, **kwargs)
        print("after super init")
        self._initialize(_INIT_SEQUENCE)

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

        print("inside _initialize()")

        # initialize the pygame module
        pygame.init()  # pylint: disable=no-member
        # load and set the logo

        if self._icon:
            print(f"loading icon: {self._icon}")
            icon = pygame.image.load(self._icon)
            pygame.display.set_icon(icon)

        if self._caption:
            pygame.display.set_caption(self._caption)

        # create the screen; must happen on main thread on macOS
        self._pygame_screen = pygame.display.set_mode(
            size=(self.width, self.height), flags=self._flags
        )

        #time.sleep(3)
        # just start the pygame-refresh loop
        self._pygame_display_thread = threading.Thread(
            target=self._pygame_refresh, daemon=True
        )
        self._pygame_display_thread.start()

    def _pygame_refresh(self):
        while not self._pygame_display_tevent.is_set():
            if not self._auto_refresh and not self._pygame_display_force_update:
                pygame.display.flip()
                continue
            time.sleep(1 / self._native_frames_per_second)
            self._refresh_display()


    def _refresh_area(self, area) -> bool:
        """Loop through dirty areas and redraw that area."""

        # pylint: disable=too-many-locals, too-many-branches

        def rgb_to_surface(buff, size):
            """convert RGB 565 buffer data to pygame Image"""
            arr = np.fromstring(buff, dtype=np.uint16)
            arr = arr.view(arr.dtype.newbyteorder('S'))
            r = (((arr & 0xF800) >> 11) * 255.0 / 31.0).astype(np.uint8)
            g = (((arr & 0x07E0) >> 5) * 255.0 / 63.0).astype(np.uint8)
            b = (((arr & 0x001F) >> 0) * 255.0 / 31.0).astype(np.uint8)
            arr = np.column_stack((r, g, b)).flat[0:]
            return pygame.image.frombuffer(arr, size, 'RGB')

        # print("INSIDE overridden _refresh_area()")
        # print("area: ")
        # print(area)
        clipped = Area()
        # Clip the area to the display by overlapping the areas.
        # If there is no overlap then we're done.
        if not self._core.clip_area(area, clipped):
            return True

        rows_per_buffer = clipped.height()
        pixels_per_word = 32 // self._core.colorspace.depth
        pixels_per_buffer = clipped.size()

        # We should have lots of memory
        buffer_size = clipped.size() // pixels_per_word

        subrectangles = 1
        # for SH1107 and other boundary constrained controllers
        #      write one single row at a time
        if self._core.sh1107_addressing:
            subrectangles = rows_per_buffer // 8
            rows_per_buffer = 8
        elif clipped.size() > buffer_size * pixels_per_word:
            rows_per_buffer = buffer_size * pixels_per_word // clipped.width()
            if rows_per_buffer == 0:
                rows_per_buffer = 1
            # If pixels are packed by column then ensure rows_per_buffer is on a byte boundary
            if (
                    self._core.colorspace.depth < 8
                    and self._core.colorspace.pixels_in_byte_share_row
            ):
                pixels_per_byte = 8 // self._core.colorspace.depth
                if rows_per_buffer % pixels_per_byte != 0:
                    rows_per_buffer -= rows_per_buffer % pixels_per_byte
            subrectangles = clipped.height() // rows_per_buffer
            if clipped.height() % rows_per_buffer != 0:
                subrectangles += 1
            pixels_per_buffer = rows_per_buffer * clipped.width()
            buffer_size = pixels_per_buffer // pixels_per_word
            if pixels_per_buffer % pixels_per_word:
                buffer_size += 1
        mask_length = (pixels_per_buffer // 32) + 1  # 1 bit per pixel + 1
        remaining_rows = clipped.height()

        for subrect_index in range(subrectangles):
            subrectangle = Area(
                x1=clipped.x1,
                y1=clipped.y1 + rows_per_buffer * subrect_index,
                x2=clipped.x2,
                y2=clipped.y1 + rows_per_buffer * (subrect_index + 1),
            )
            if remaining_rows < rows_per_buffer:
                subrectangle.y2 = subrectangle.y1 + remaining_rows
            remaining_rows -= rows_per_buffer

            buffer = memoryview(bytearray([0] * (buffer_size * 4)))  # .cast("I")
            mask = memoryview(bytearray([0] * (mask_length * 4))).cast("I")
            self._core.fill_area(subrectangle, mask, buffer)

            image_surface = rgb_to_surface(bytes(buffer), (subrectangle.width(), subrectangle.height()))
            self._pygame_screen.blit(image_surface, (subrectangle.x1, subrectangle.y1))
            pygame.display.flip()
            time.sleep(0.1)
            
        return True

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
        except pygame.error as e:
            print("pygame error during check_quit()")
            print(traceback.format_exc())
            return True
        return False

    def event_loop(self, interval=None, on_time=None, on_event=None, events=None):
        """
        pygame event-loop. Has to be called by the main thread. This method
        terminates in case of a QUIT-event. An optional callback on_time is
        executed every interval seconds. Use this callback for
        application specific logic.
        """
        print(".")
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

    # @property
    # def root_group(self):
    #     """
    #     The root group on the display. If the root group is set to None, no output will be shown.
    #     """
    #     return self._root_group
    #
    # @root_group.setter
    # def root_group(self, group):
    #     self._root_group = group
    #     #self.show(group)
