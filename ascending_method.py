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

import sys
import logging
from audiometer import controller
from audiometer import audiogram


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s',
                    handlers=[logging.FileHandler("logfile.log", 'w'),
                              logging.StreamHandler()])


class AscendingMethod:

    def __init__(self):
        self.ctrl = controller.Controller()
        self.current_level = 0
        self.click = True

    def decrement_click(self, level_decrement):

        self.current_level -= level_decrement
        self.click = self.ctrl.clicktone(self.freq, self.current_level,
                                         self.earside)

    def increment_click(self, level_increment):

        self.current_level += level_increment
        self.click = self.ctrl.clicktone(self.freq, self.current_level,
                                         self.earside)

    def familiarization(self):
        logging.info("Begin Familiarization")

        print("\nSet a clearly audible tone "
              "via the arrow keys (up & down) on the keyboard.\nConfirm "
              "with the Enter Key\n")

        self.current_level = self.ctrl.audibletone(
                             self.freq,
                             self.ctrl.config.beginning_fam_level,
                             self.earside)

        print("\nTo begin, click once")
        self.ctrl.wait_for_click()

        while self.click:
            logging.info("-%s", self.ctrl.config.large_level_decrement)
            self.decrement_click(self.ctrl.config.large_level_decrement)

        while not self.click:
            logging.info("+%s", self.ctrl.config.large_level_increment)
            self.increment_click(self.ctrl.config.large_level_increment)

    def hearing_test(self):
        self.familiarization()

        logging.info("End Familiarization: -%s",
                     self.ctrl.config.small_level_decrement)
        self.decrement_click(self.ctrl.config.small_level_decrement)

        while not self.click:
            logging.info("+%s", self.ctrl.config.small_level_increment)
            self.increment_click(self.ctrl.config.small_level_increment)

        current_level_list = []
        current_level_list.append(self.current_level)

        three_answers = False
        while not three_answers:
            logging.info("3of5?: %s", current_level_list)
            for x in range(4):
                while self.click:
                    logging.info("-%s", self.ctrl.config.small_level_decrement)
                    self.decrement_click(
                        self.ctrl.config.small_level_decrement)

                while not self.click:
                    logging.info("+%s", self.ctrl.config.small_level_increment)
                    self.increment_click(
                        self.ctrl.config.small_level_increment)

                current_level_list.append(self.current_level)
                logging.info("3of5?: %s", current_level_list)
                # http://stackoverflow.com/a/11236055
                if [k for k in current_level_list
                   if current_level_list.count(k) == 3]:
                    three_answers = True
                    logging.info("3of5 --> True")
                    break
            else:
                logging.info("No Match! --> +%s",
                             self.ctrl.config.large_level_increment)
                current_level_list = []
                self.increment_click(self.ctrl.config.large_level_increment)

    def run(self):

        if not self.ctrl.config.logging:
            logging.disable(logging.CRITICAL)

        for self.earside in self.ctrl.config.earsides:
            for self.freq in self.ctrl.config.freqs:
                logging.info('freq:%s earside:%s', self.freq, self.earside)
                try:
                    self.hearing_test()
                    self.ctrl.save_results(self.current_level, self.freq,
                                           self.earside)

                except OverflowError:
                    print("The signal is distorted. Possible causes are "
                          "an incorrect calibration or a severe hearing "
                          "loss. I'm going to the next frequency.")
                    self.current_level = None
                    continue

                except KeyboardInterrupt:
                    sys.exit('\nInterrupted by user')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.ctrl.__exit__()
        audiogram.make_audiogram(self.ctrl.config.filename,
                                 self.ctrl.config.results_path)

if __name__ == '__main__':

    with AscendingMethod() as asc_method:
        asc_method.run()

    print("Finished!")