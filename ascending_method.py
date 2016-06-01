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

import argparse
import logging
from audiometer import controller


parser = argparse.ArgumentParser()


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s',
                    handlers=[logging.FileHandler("logfile.log", 'w'),
                              logging.StreamHandler()])


class AscendingMethod:

    def __init__(self, freq, earside):
        self.freq = freq
        self.earside = earside
        self.current_level = 0
        self.click = False

    def decrement_click(self, level_decrement):

        self.current_level -= level_decrement
        self.click = ctrl.clicktone(self.freq, self.current_level, self.earside)

    def increment_click(self, level_increment):

        self.current_level += level_increment
        self.click = ctrl.clicktone(self.freq, self.current_level, self.earside)


def familiarization():
    logging.info("Begin Familiarization")

    while not asc_method.click:
        (asc_method.click,
         asc_method.current_level) = ctrl.clicktone(asc_method.freq, -1,
                                                  asc_method.earside,
                                                  attack=1000000,
                                                  timeout=15,
                                                  fam=True)

    while asc_method.click:
        logging.info("-%s", ctrl.config.large_level_decrement)
        asc_method.decrement_click(ctrl.config.large_level_decrement)

    while not asc_method.click:
        logging.info("+%s", ctrl.config.large_level_increment)
        asc_method.increment_click(ctrl.config.large_level_increment)


def hearing_test():
    familiarization()

    logging.info("End Familiarization: -%s", ctrl.config.small_level_decrement)
    asc_method.decrement_click(ctrl.config.small_level_decrement)

    while not asc_method.click:
        logging.info("+%s", ctrl.config.small_level_increment)
        asc_method.increment_click(ctrl.config.small_level_increment)

    current_level_list = []
    current_level_list.append(asc_method.current_level)

    three_answers = False
    while not three_answers:
        logging.info("3of5?: %s", current_level_list)
        for x in range(4):
            while asc_method.click:
                logging.info("-%s", ctrl.config.small_level_decrement)
                asc_method.decrement_click(ctrl.config.small_level_decrement)

            while not asc_method.click:
                logging.info("+%s", ctrl.config.small_level_increment)
                asc_method.increment_click(ctrl.config.small_level_increment)

            current_level_list.append(asc_method.current_level)
            logging.info("3of5?: %s", current_level_list)
            # http://stackoverflow.com/a/11236055
            if [k for k in current_level_list
                if current_level_list.count(k) == 3]:
                three_answers = True
                logging.info("3of5 --> True")
                break
        else:
            logging.info("No Match! --> +%s", ctrl.config.large_level_increment)
            current_level_list = []
            asc_method.increment_click(ctrl.config.large_level_increment)


with controller.Controller() as ctrl:
    if not ctrl.config.logging:
        logging.disable(logging.CRITICAL)

    for earside in ctrl.config.earsides:
        for freq in ctrl.config.freqs:
            logging.info('freq:%s earside:%s', freq, earside)
            asc_method = AscendingMethod(freq, earside)
            try:
                hearing_test()
                ctrl.save_results(asc_method.current_level, asc_method.freq,
                                  asc_method.earside)

            except OverflowError:
                print("The signal is distorted. Possible causes are an "
                      "incorrect calibration or a severe hearing loss. "
                      "I'm going to the next frequency.")
                continue

            except KeyboardInterrupt:
                parser.exit('\nInterrupted by user')