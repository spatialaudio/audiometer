#!/usr/bin/env python3
"""Ascending method.

For more details about the 'ascending method', have a look at
https://github.com/franzpl/audiometer/blob/master/docu/docu_audiometer.ipynb
The 'ascending method' is described in chapter 3.1.1

**WARNING**: If the hearing loss is too severe, this method will
not work! Please, consult an audiologist!

**WARNUNG**: Bei extremer Schwerhörigkeit ist dieses Verfahren nicht
anwendbar! Bitte suchen Sie einen Audiologen auf!

"""

from audiometer import tone_generator
from audiometer import responder
from configparser import ConfigParser
import time
import random

cfg1 = ConfigParser()
cfg2 = ConfigParser()

cfg1.read('config.ini')
device = int(cfg1['Device']['device'])
calibration_factor = float(cfg1['AudiometerCalibration']['calibration_factor'])
attack = int(cfg1['FadeIn/FadeOut Time']['attack'])
release = int(cfg1['FadeIn/FadeOut Time']['release'])
timeout = int(cfg1['Timeout']['timeout'])
responder_device = cfg1['Responder']['responder_device']
# http://stackoverflow.com/a/30223001
str_freqs = cfg1.get('Standard Frequencies', 'freqs').split('\n')

# "The order of presentation of test tones when the audiometer settings are
# performed manually shall be from
# 1 000 Hz upwards, followed by the lower frequency range, in descending order.
# A repeat test shall be carried
# out at 1 000 Hz on the ear tested first." (ISO 8253-1 chapter 6.1)
freqs = [int(i) for i in str_freqs]

cfg2.read('results.ini')
familiar_result = int(cfg2['Familiarization']['familiar_result'])


increase_5db = 5
increase_10db = 10
decrease_10db = 10
i = 0  # counter
current_level_list = []
three_answers = False


def process(freq, level, earside):
    if level >= 0:
        raise OverflowError("Maybe your hearing loss is too severe for "
        "this method. Please, consult an audiologist!")
    audio.start(freq, level, earside=earside)
    click = rpd.wait_for_click()
    audio.stop()
    time.sleep(timeout + random.random())  # described in chapter 3.1
    return click

# Step 1

with tone_generator.AudioStream(device, attack, release) as audio, (
     responder.MouseResponder(timeout, responder_device)) as rpd:

    earside = 'right'
    freq_1000 = freqs[4]
    current_level = familiar_result - decrease_10db
    click = process(freq_1000, familiar_result, earside)

    while not click:
        current_level += increase_5db
        click = process(freq_1000, current_level, earside)
# Step 2

    while not three_answers:
        for x in range(5):
            while click:
                current_level -= decrease_10db
                click = process(freq_1000, current_level, earside)

            while not click:
                current_level += increase_5db
                click = process(freq_1000, current_level, earside)
            current_level_list.append(current_level)
            # http://stackoverflow.com/a/11236055
            if [x for x in current_level_list if current_level_list.count(x) == 3]:
                three_answers = True
                break
        else:
            current_level += increase_10db
            current_level_list = []







