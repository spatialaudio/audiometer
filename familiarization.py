#!/usr/bin/env python3
"""Familiarization.

For more details about the familiarization, have a look at
https://github.com/franzpl/audiometer/blob/master/docu/docu_audiometer.ipynb
The familiarization is described in chapter 2 and 3.

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

print("Start familiarization on the right ear \n")
time.sleep(1)

earside = 'right'
timeout = 2  # described in chapter 3.1
start_level = -40  # dB
decreasing_tone = 20  # dB
increasing_tone = 10  # dB
familiar_freq = 1000  # Hz


with tone_generator.AudioStream(device, attack, release) as audio, (
     responder.MouseResponder()) as rpd:

    audio.start(familiar_freq, start_level, earside=earside)
    click = rpd.wait_for_click(timeout)
    audio.stop()
    time.sleep(timeout + random.random())  # described in chapter 3.1
    current_level = start_level
    while not click:  # increasing tone
            audio.start(familiar_freq, current_level + increasing_tone,
                        earside=earside)
            click = rpd.wait_for_click(timeout)
            audio.stop()
            current_level += increasing_tone
            time.sleep(timeout + random.random())
    while click:  # decreasing tone
            audio.start(familiar_freq, current_level - decreasing_tone,
                        earside=earside)
            click = rpd.wait_for_click(timeout)
            audio.stop()
            current_level -= decreasing_tone
            time.sleep(timeout + random.random())
    with open('results.ini', 'w') as res:  # save the level for further tests
        cfg2.add_section('Familiarization')
        cfg2.set('Familiarization', 'familiar_result', str(current_level))
        cfg2.write(res)

    while not click:  # increasing tone
            audio.start(familiar_freq, current_level + increasing_tone,
                        earside=earside)
            click = rpd.wait_for_click(timeout)
            audio.stop()
            current_level += increasing_tone
            time.sleep(timeout + random.random())

    print("Presenting the last heard tone\n")
    time.sleep(1)
    audio.start(familiar_freq, current_level, earside=earside)
    rpd.wait_for_click(timeout)
    audio.stop()
    print("End of familiarization on the right ear\n")
    rpd.close()
    audio.close()
