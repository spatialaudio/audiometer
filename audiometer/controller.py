from audiometer import tone_generator
from audiometer import responder
import csv
import time
import random
from audiometer import config_loader
import os


class Controller:

    def __init__(self):

        self._cfg = config_loader.Config()
        self.freqs = self._cfg.freqs

        if self._cfg.earside == 'right':
            earside_contralateral = 'left'
        elif self._cfg.earside == 'left':
            earside_contralateral = 'right'
        else:
            raise ValueError("earside_beginning must be 'right' or 'left'")
        self.earside_order = self._cfg.earside, earside_contralateral

        self.small_level_increment = self._cfg.small_level_increment
        self.large_level_increment = self._cfg.large_level_increment
        self.small_level_decrement = self._cfg.small_level_decrement
        self.large_level_decrement = self._cfg.large_level_decrement

        self.start_level_familiar = self._cfg.start_level_familiar

        path = 'audiometer/results'
        if not os.path.exists(path):
            os.makedirs(path)
        filename = ('result_{}'.format(time.strftime("%d.%m.%Y_%H:%M:%S")) +
                   '.csv')
        self._csvfile = open(os.path.join(path, filename), 'w')
        self._writer = csv.writer(self._csvfile)
        self._writer.writerow(['Familiarization Result/dB', 'Level/dB',
                               'Frequency/Hz', 'Earside'])

        self._audio = tone_generator.AudioStream(self._cfg.device,
                                                 self._cfg.attack,
                                                 self._cfg.release)
        self._rpd = responder.Responder(self._cfg.timeout,
                                        self._cfg.responder_device)

    def process(self, freq, level, earside):
        if level >= 0:
            raise OverflowError("The signal is distorted. Possible causes are "
            "an incorrect calibration or a severe hearing loss. I'm going "
            "to the next frequency")
        self._audio.start(freq, level, earside)
        click = self._rpd.wait_for_click()
        self._audio.stop()
        time.sleep(self._cfg.timeout + random.random())
        return click

    def save_results(self, familiar_result, level, freq, earside):
        row = [familiar_result, level, freq, earside]
        self._writer.writerow(row)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        time.sleep(0.1)
        self._rpd.close()
        self._audio.close()
        self._csvfile.close()

