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


from audiometer import controller
from audiometer import familiarization


def decrement_click(current_level, level_decrement):

    current_level -= level_decrement
    click = ctrl.process(freq, current_level, earside)
    return current_level, click


def increment_click(current_level, level_increment):

    current_level += level_increment
    click = ctrl.process(freq, current_level, earside)
    return current_level, click


def step1(freq, start_level_familiar, earside):
    familiar_result = familiarization.fam(ctrl, freq, large_level_increment,
                                          large_level_decrement,
                                          start_level_familiar, earside)

    current_level, click = decrement_click(familiar_result,
                                           small_level_decrement)

    while not click:
        increment_click(current_level, small_level_increment)
    return current_level, familiar_result, click


def step2(click, current_level, freq, earside):
    three_answers = False
    while not three_answers:
        current_level_list = []
        for x in range(5):
            while click:
                current_level, click = decrement_click(current_level,
                                                       small_level_decrement)
            while not click:
                current_level, click = increment_click(current_level,
                                                       small_level_increment)
            current_level_list.append(current_level)
            # http://stackoverflow.com/a/11236055
            if [k for k in current_level_list
                if current_level_list.count(k) == 3]:
                three_answers = True
                break
        else:
            current_level += large_level_increment
        return current_level


with controller.Controller() as ctrl:

    freq_list = ctrl.freqs

    earside_order = ctrl.earside_order

    small_level_increment = ctrl.small_level_increment
    large_level_increment = ctrl.large_level_increment
    small_level_decrement = ctrl.small_level_decrement
    large_level_decrement = ctrl.large_level_decrement

    start_level_familiar = ctrl.start_level_familiar

    for earside in earside_order:
        i = 0
        for freq in freq_list[i:]:
            try:
                current_level, familiar_result, click = step1(freq,
                                                          start_level_familiar,
                                                          earside)
                current_level = step2(click, current_level, freq, earside)
                ctrl.save_results(familiar_result, current_level, freq, earside)
            except OverflowError:
                jump_to_next_freq = freq_list.index(freq) + 1
                i = jump_to_next_freq

