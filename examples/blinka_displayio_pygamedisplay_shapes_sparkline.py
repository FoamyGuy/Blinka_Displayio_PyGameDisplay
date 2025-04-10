# SPDX-FileCopyrightText: 2020 Kevin Matocha, Tim C
#
# SPDX-License-Identifier: Unlicense
"""
This example has been adapted from the example in the shapes
library to work with pygame display.
"""

# class of sparklines in CircuitPython
# created by Kevin Matocha - Copyright 2020 (C)

# See the bottom for a code example using the `sparkline` Class.

# # File: display_shapes_sparkline.py
# A sparkline is a scrolling line graph, where any values added to sparkline
# using `add_value` are plotted.
#
# The `sparkline` class creates an element suitable for adding to the display
# using `display.root_group = mySparkline` or adding to a `displayio.Group` to be displayed.
#
# When creating the sparkline, identify the number of `max_items` that will be
# included in the graph.
# When additional elements are added to the sparkline and the number of items
# has exceeded max_items, any excess values are removed from the left of the
# graph, and new values are added to the right.


# The following is an example that shows the

# setup display
# instance sparklines
# add to the display
# Loop the following steps:
# 	add new values to sparkline `add_value`
# 	update the sparklines `update`


import random
import time
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.sparkline import Sparkline
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
from blinka_displayio_pygamedisplay import PyGameDisplay


##########################################
# Create background bitmaps and sparklines
##########################################

display = PyGameDisplay(icon="blinka.png", width=640, height=480)

# Baseline size of the sparkline chart, in pixels.
chart_width = display.width - 50
chart_height = display.height - 50

font = terminalio.FONT

LINE_COLOR = 0xFFFFFF

# Setup the first bitmap and sparkline
# This sparkline has no background bitmap
# mySparkline1 uses a vertical y range between 0 to 10 and will contain a
# maximum of 40 items
sparkline1 = Sparkline(
    width=chart_width,
    height=chart_height,
    max_items=40,
    y_min=0,
    y_max=10,
    x=40,
    y=30,
    color=LINE_COLOR,
)

# Label the y-axis range

TEXT_XOFFSET = -10
text_label1a = label.Label(
    font=font, text=str(sparkline1.y_top), color=LINE_COLOR
)  # yTop label
text_label1a.anchor_point = (1, 0.5)  # set the anchorpoint at right-center
text_label1a.anchored_position = (
    sparkline1.x + TEXT_XOFFSET,
    sparkline1.y,
)  # set the text anchored position to the upper right of the graph

text_label1b = label.Label(
    font=font, text=str(sparkline1.y_bottom), color=LINE_COLOR
)  # yTop label
text_label1b.anchor_point = (1, 0.5)  # set the anchorpoint at right-center
text_label1b.anchored_position = (
    sparkline1.x + TEXT_XOFFSET,
    sparkline1.y + chart_height,
)  # set the text anchored position to the upper right of the graph


bounding_rectangle = Rect(
    sparkline1.x, sparkline1.y, chart_width, chart_height, outline=LINE_COLOR
)


# Create a group to hold the sparkline, text, rectangle and tickmarks
# append them into the group (my_group)
#
# Note: In cases where display elements will overlap, then the order the
# elements are added to the group will set which is on top.  Latter elements
# are displayed on top of former elemtns.

my_group = displayio.Group()

my_group.append(sparkline1)
my_group.append(text_label1a)
my_group.append(text_label1b)
my_group.append(bounding_rectangle)

TOTAL_TICKS = 10

for i in range(TOTAL_TICKS + 1):
    x_start = sparkline1.x - 5
    x_end = sparkline1.x
    y_both = int(round(sparkline1.y + (i * (chart_height) / (TOTAL_TICKS))))
    if y_both > sparkline1.y + chart_height - 1:
        y_both = sparkline1.y + chart_height - 1
    my_group.append(Line(x_start, y_both, x_end, y_both, color=LINE_COLOR))


# Set the display to show my_group that contains the sparkline and other graphics
display.root_group = my_group

# Start the main loop
while True:

    # Turn off auto_refresh to prevent partial updates of the screen during updates
    # of the sparkline drawing
    # display.auto_refresh = False

    # add_value: add a new value to a sparkline
    # Note: The y-range for mySparkline1 is set to 0 to 10, so all these random
    # values (between 0 and 10) will fit within the visible range of this sparkline
    sparkline1.add_value(random.uniform(0, 10))

    display.refresh()

    # The display seems to be less jittery if a small sleep time is provided
    # You can adjust this to see if it has any effect
    time.sleep(0.01)

    if display.check_quit():
        break
