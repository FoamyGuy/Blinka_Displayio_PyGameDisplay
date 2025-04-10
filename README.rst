Introduction
============

.. image:: https://readthedocs.org/projects/blinka_displayio_pygamedisplay/badge/?version=stable
    :target: https://blinka-displayio-pygamedisplay.readthedocs.io/en/stable/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/foamyguy/Blinka_Displayio_PyGameDisplay/workflows/Build%20CI/badge.svg
    :target: https://github.com/foamyguy/Blinka_Displayio_PyGameDisplay/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

.. image:: https://github.com/FoamyGuy/Blinka_Displayio_PyGameDisplay/blob/main/banner.png?raw=true
    :alt: PyGame + Blinka

VERSION NOTICE
==============
This library has not been updated to work with Blinka_DisplayIO 1.0.0+ yet. The most recent version of Bliaka_DisplayIO that is supported is 0.11.1.

Info
====

Blinka makes her debut on the big screen! With this library you can use CircuitPython ``displayio`` code on PC and Raspberry Pi to output to a PyGame window instead of a hardware display connected to I2C or SPI. This makes it easy to to use ``displayio`` elements on HDMI and other large format screens.

Warning: you must check ``display.check_quit()`` in the main loop and ``break`` if it's true in order to correctly handle the close button!

Dependencies
=============
This driver depends on:

* `PyGame <https://github.com/pygame/pygame>`_
* `Adafruit Blinka Displayio <https://github.com/adafruit/Adafruit_Blinka_Displayio>`_

Please ensure all dependencies are available they can be installed with pip3


Optional Dependencies
=====================
This driver can optionally make use of these ``displayio`` module libraries:

* `Adafruit Display Text <https://github.com/adafruit/Adafruit_CircuitPython_Display_Text>`_
* `Adafruit ImageLoad <https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad>`_
* `Adafruit Progress Bar <https://github.com/adafruit/Adafruit_CircuitPython_ProgressBar>`_
* `Adafruit Display Button <https://github.com/adafruit/Adafruit_CircuitPython_Display_Button>`_

They can be installed with pip3.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-blinka_displayio_pygamedisplay/>`_. To install for current user:

.. code-block:: shell

    pip3 install blinka-displayio-pygamedisplay

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install blinka-displayio-pygamedisplay

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install blinka-displayio-pygamedisplay

Usage Example
=============

.. code-block:: python

    import displayio
    from blinka_displayio_pygamedisplay import PyGameDisplay

    display = PyGameDisplay(width=320, height=240)
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(display.width, display.height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0x00FF00  # Bright Green

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    # Must check display.running in the main loop!

    while True:
        if display.check_quit():
            break

Initialization Parameters
=========================

* ``width`` (required) - The width of the window. A value of zero maximizes the window
* ``height`` (required) - The height of the window. A value of zero maximizes the window
* ``icon`` (optional) - An icon for the PyGame window
* ``caption`` (optional) - A caption for the PyGame window
* ``native_frames_per_second`` (optional) - High values result in high CPU load
* ``scale`` (optional) - A positive scaling factor for the window. Default is 1
* ``hw_accel`` (optional) - Whether to use hardware acceleration. Default is True
* ``flags`` (optional) - Pygame display flags, e.g. pygame.FULLSCREEN or pygame.NOFRAME

Scale can be used to make smaller displays easier to see on high resolution displays.
The actual window dimensions are ``width * scale`` by ``height * scale``, however the display dimensions remain ``width`` by ``height``.

To ensure pixel accuracy of the display, only integer upscaling is supported (``scale >= 1``).

If you encounter GL or EGL Pygame errors, try setting ``hw_accel`` to False to disable hardware acceleration. Performance may be reduced.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/foamyguy/Foamyguy_CircuitPython_Blinka_Displayio_PyGameDisplay/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
