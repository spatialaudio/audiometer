#!/usr/bin/env python3
"""Familiarization.

For more details about the familiarization, have a look at
https://github.com/franzpl/audiometer/blob/master/docu/docu_audiometer.ipynb
The familiarization is described in chapter 2 and 3.

**WARNING**: If the hearing loss is too severe, this familiarization will
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


print("Start familiarization on the right ear \n")
time.sleep(1)

earside = 'right'
start_level = -40  # dB
decreasing_tone = 20  # dB
increasing_tone = 10  # dB
familiar_freq = 1000  # Hz


def process(freq, level):
    if level >= 0:
        raise OverflowError("Maybe your hearing loss is too severe for "
        "the familiarization. Please, consult an audiologist!")
    audio.start(freq, level, earside=earside)
    click = rpd.wait_for_click()
    audio.stop()
    time.sleep(timeout + random.random())  # described in chapter 3.1
    return click


def save_results(level):
    with open('results.ini', 'w') as res:  # save the level for further tests
        cfg2.add_section('Familiarization')
        cfg2.set('Familiarization', 'familiar_result', str(current_level))
        cfg2.write(res)

with tone_generator.AudioStream(device, attack, release) as audio, (
     responder.MouseResponder(timeout, responder_device)) as rpd:

    click = process(familiar_freq, start_level)
    current_level = start_level

    while not click:  # increasing tone
            current_level += increasing_tone
            click = process(familiar_freq, current_level)
    while click:  # decreasing tone
            current_level -= decreasing_tone
            click = process(familiar_freq, current_level)

    save_results(current_level)

    while not click:  # increasing tone
            current_level += increasing_tone
            click = process(familiar_freq, current_level)

    print("Presenting the last heard tone\n")
    time.sleep(1)
    process(familiar_freq, current_level)
    print("End of familiarization on the right ear\n")
    rpd.close()
    audio.close()
