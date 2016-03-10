#!/usr/bin/env python3

import tone_generator
import time
import pyxhook_responder


device = 0
timeout = 3  # seconds
fade_in = 30  # ms
fade_out = 40  # ms

audio = tone_generator.AudioStream(device, fade_in, fade_out)  # open stream
rpd = pyxhook_responder.MouseResponder()  # initialize MouseResponder
time.sleep(2)
audio.start(20000, -10, earside='')  # start first tone
click = rpd.wait_for_click(timeout)  # you have x seconds to click
audio.stop(fade_out)  # stop tone

time.sleep(2)

if click:
    frequency, level = 20000, -10
else:
    frequency, level = 20000, -10
audio.start(frequency, level, earside='')

click = rpd.wait_for_click(timeout)
audio.stop(fade_out)
time.sleep(2)
rpd.close()
audio.close()
