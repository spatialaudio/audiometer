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


def step1(freq, increase_10db, decrease_20db, start_level_familiar, earside):
    familiar_result = familiarization.fam(ctrl, freq, increase_10db,
                                          decrease_20db, start_level_familiar,
                                          earside)
    current_level = familiar_result - decrease_10db
    click = ctrl.process(freq, familiar_result, earside)
    while not click:
        current_level += increase_5db
        click = ctrl.process(freq, current_level, earside)
    return current_level, familiar_result, click


def step2(click, current_level, freq, earside):
    three_answers = False
    while not three_answers:
        current_level_list = []
        for x in range(5):
            while click:
                current_level -= decrease_10db
                click = ctrl.process(freq, current_level, earside)

            while not click:
                current_level += increase_5db
                click = ctrl.process(freq, current_level, earside)
            current_level_list.append(current_level)
            # http://stackoverflow.com/a/11236055
            if [k for k in current_level_list
                if current_level_list.count(k) == 3]:
                three_answers = True
                break
        else:
            current_level += increase_10db
        return current_level


with controller.Controller() as ctrl:
    freq_list = ctrl.get_freqs()
    earside_order = ctrl.get_earside()
    (increase_5db, increase_10db, decrease_10db,
    decrease_20db) = ctrl.get_increases_decreases()
    start_level_familiar = ctrl.get_start_level_familiar()
    for earside in earside_order:
        for freq in freq_list:
            current_level, familiar_result, click = step1(freq, increase_10db,
                                                          decrease_20db,
                                                          start_level_familiar,
                                                          earside)
            current_level = step2(click, current_level, freq, earside)
            ctrl.save_results(familiar_result, current_level, freq, earside)



