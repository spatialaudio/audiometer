#!/usr/bin/env python3

from audiometer import tone_generator
from audiometer import responder
import time


device = 0
timeout = 2  # seconds
attack = 30  # ms
release = 40  # ms

audio = tone_generator.AudioStream(device, attack, release)  # open stream
rpd = responder.MouseResponder()  # initialize MouseResponder
audio.start(500, -10, earside='right')  # start first tone
click = rpd.wait_for_click(timeout)  # you have x seconds to click
audio.stop()  # stop tone
time.sleep(2)
if click:
    frequency, level = 1000, -15
else:
    frequency, level = 2000, -20
audio.start(frequency, level, earside='left')
click = rpd.wait_for_click(timeout)
audio.stop()
time.sleep(0.5)
rpd.close()
audio.close()
