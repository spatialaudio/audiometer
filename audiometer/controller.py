from audiometer import tone_generator
from audiometer import responder
import csv
import time
import random
from audiometer import config_loader


class Controller:

    def __init__(self):
        (device, attack, release, self.timeout, self.freqs, self.increase_5db,
        self.increase_10db, self.decrease_10db, self.decrease_20db,
        self.start_level_familiar, self.earside_beginning,
        responder_device) = config_loader.load()

        self._csvfile = open('results.csv', 'w')
        self._writer = csv.writer(self._csvfile)
        self._writer.writerow(['Familiarization Result / dB', 'Level / dB',
                               'Frequency / Hz', 'Earside'])

        self._audio = tone_generator.AudioStream(device, attack, release)
        self._rpd = responder.Responder(self.timeout, responder_device)

    def get_increases_decreases(self):
        return (self.increase_5db, self.increase_10db, self.decrease_10db,
                self.decrease_20db)

    def get_start_level_familiar(self):
        return self.start_level_familiar

    def get_freqs(self):
        return self.freqs

    def get_earside(self):
        if self.earside_beginning == 'right':
            earside_contralateral = 'left'
        elif self.earside_beginning == 'left':
            earside_contralateral = 'right'
        else:
            raise ValueError("earside_beginning must be 'right' or 'left'")
        return self.earside_beginning, earside_contralateral

    def process(self, freq, level, earside):
        if level >= 0:
            raise OverflowError("The signal is distorted. Possible causes are "
            "an incorrect calibration or a severe hearing loss")
        self._audio.start(freq, level, earside)
        click = self._rpd.wait_for_click()
        self._audio.stop()
        time.sleep(self.timeout + random.random())
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

