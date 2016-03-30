#!/usr/bin/env python3

import tone_generator
import time
import pyxhook_responder


device = 0
timeout = 2  # seconds
fade_in = 30  # ms
fade_out = 40  # ms

audio = tone_generator.AudioStream(device, fade_in, fade_out)  # open stream
rpd = pyxhook_responder.MouseResponder()  # initialize MouseResponder
audio.start(500, -10, earside='right')  # start first tone
click = rpd.wait_for_click(timeout)  # you have x seconds to click
audio.stop()  # stop tone
if click:
    frequency, level = 1000, -40
else:
    frequency, level = 2000, -25
audio.start(frequency, level, earside='left')

click = rpd.wait_for_click(timeout)
audio.stop()
rpd.close()
audio.close()
audio.plotting_output()
