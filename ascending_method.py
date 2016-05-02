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

ctrl = controller.Controller()

freq_list = ctrl._freq_list()
earside_order = ctrl._earside()  # ('right' & 'left') or ('left' & 'right')


increase_5db = 5  # dB
increase_10db = 10  # dB
decrease_10db = 10  # dB


for earside in earside_order:
    for freq in freq_list:

# Step 1
        familiar_result = familiarization.fam(ctrl, freq, earside)
        current_level = familiar_result - decrease_10db
        click = ctrl._process(freq, familiar_result, earside)
        while not click:
            current_level += increase_5db
            click = ctrl._process(freq, current_level, earside)
# Step 2
        three_answers = False
        while not three_answers:
            current_level_list = []
            for x in range(5):
                while click:
                    current_level -= decrease_10db
                    click = ctrl._process(freq, current_level, earside)

                while not click:
                    current_level += increase_5db
                    click = ctrl._process(freq, current_level, earside)
                current_level_list.append(current_level)
                # http://stackoverflow.com/a/11236055
                if [k for k in current_level_list
                if current_level_list.count(k) == 3]:
                    three_answers = True
                    break
            else:
                current_level += increase_10db
        ctrl._save_results(current_level, freq, earside,
            'Ascending Method Results')


# Step 3

ctrl._exit()