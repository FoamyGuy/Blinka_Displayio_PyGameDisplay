# SPDX-FileCopyrightText: Copyright (c) 2026 Bernhard Bablok
#
# SPDX-License-Identifier: MIT

"""
`keypad_pygame`
================================================================================

Mimic behavior of native keypad module.

* Author(s): Bernhard Bablok

"""

# pylint: disable=protected-access

# imports

import keypad
import time
import pygame

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/foamyguy/Foamyguy_CircuitPython_Blinka_Displayio_PyGameDisplay.git"


class PyGameKeys(keypad._KeysBase):
    """Manage a set of independent keys."""

    def __init__(
        self, py_keys, *, value_when_pressed, pull=True, interval=0.02, max_events=64
    ):
        # pylint: disable=unused-argument, too-many-arguments
        """
        Create a `PyGameKeys` object that will record key-presses.
        Each key is independent.

        An `EventQueue` is created when this object is created and is available in the
        `events` attribute.

        :param Sequence[keycode] py_keys: List of keycodes to monitor.
          The key numbers correspond to indices into this sequence.
          If the sequence is empty, record all key-presses.
        :param bool value_when_pressed: ``True`` if the key reads high when the key is pressed.
          ``False`` if the key reads low when the key is pressed.
          All the keys must be defined in the same way.
        :param bool pull: ``True`` (ignored)
        :param float interval: Scan keys no more often than ``interval`` to allow for debouncing.
          ``interval`` is in float seconds. The default is 0.020 (20 msecs).
        :param int max_events: maximum size of `events` `EventQueue`:
          maximum number of key transition events that are saved.
          Must be >= 1.
          If a new event arrives when the queue is full, the oldest event is discarded.
        """
        self._display = None
        self._interval = interval
        self._keycodes = py_keys
        self._value_when_pressed = value_when_pressed
        super().__init__(interval, max_events, self._keypad_keys_scan)
        self._last_scan = time.monotonic()
        self._currently_pressed = [False] * self.key_count
        self._previously_pressed = [False] * self.key_count

    def deinit(self):
        """Stop scanning"""
        if self._display:
            self._display._keypad.deinit()
            self._display = None
        super().deinit()

    def reset(self):
        """Reset the internal state of the scanner to assume that all keys are now released.
        Any key that is already pressed at the time of this call will therefore immediately cause
        a new key-pressed event to occur.
        """

    @property
    def key_count(self):
        """The number of keys that are being scanned. (read-only)"""
        return len(self._keycodes)

    def _scanning_loop(self):
        """This is called in a thread. Use a no-op implementation,
        since the PyGame event-loop registers key-events directly"""
        while True:
            time.sleep(self._interval)

    def _keypad_keys_scan(self):
        """Never called, since we override _scanning_loop"""

    def _check(self, pygame_ev):
        """Check the given pygame-event for a key in our list.
        This method is called from the PyGame event-queue"""
        elapsed = time.monotonic() - self._last_scan
        if self._interval - elapsed > 0:
            # simulate _scanning_loop: every self._interval
            return
        self._last_scan = time.monotonic()
        # check keys (record all keys if list of keys is empty)
        keys = (
            enumerate(self._keycodes)
            if self._keycodes
            else [(pygame_ev.key, pygame_ev.key)]
        )
        for key_number, keycode in keys:
            if pygame_ev.key == keycode:
                if pygame_ev.type == pygame.KEYDOWN:
                    state = self._value_when_pressed
                else:
                    state = not self._value_when_pressed
                self._events.keypad_eventqueue_record(key_number, state)
                return
