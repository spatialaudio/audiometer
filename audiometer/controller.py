from audiometer import tone_generator
from audiometer import responder
import argparse
import time
import os
import csv
import random
import numpy as np


def config():

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--device", help='How to select your soundcard is '
    'shown in http://python-sounddevice.readthedocs.org/en/0.3.3/'
    '#sounddevice.query_devices', type=int, default=1)
    parser.add_argument("--calibration_factor", type=float, default=1)
    parser.add_argument("--responder_device", type=str,
                        default="mouse left", help='You can also'
                        'use the spacebar key. In this case enter: '
                        'spacebar')
    parser.add_argument("--attack", type=float, default=30)
    parser.add_argument("--release", type=float, default=40)
    parser.add_argument("--timeout", type=float, default=2, help='For more'
    'information on the timeout duration have a look at '
    'ISO8253-1 ch. 6.2.1')
    parser.add_argument("--earsides", type=str, nargs='+',
                        default=['right', 'left'], help="The first list item "
                        "represents the beginning earside. The second list "
                        "item represents the ending earside, consequently. "
                        "It is also possible to choose only one earside, "
                        "left or right")
    parser.add_argument("--small_level_increment", type=float, default=5)
    parser.add_argument("--large_level_increment", type=float, default=10)
    parser.add_argument("--small_level_decrement", type=float, default=10)
    parser.add_argument("--large_level_decrement", type=float, default=20)
    parser.add_argument("--start_level_familiar", type=float, default=-40)
    parser.add_argument("--freqs", type=float, nargs='+', default=[1000, 1500,
                        2000, 3000, 4000, 6000, 8000, 750, 500, 250, 125],
                        help='The size'
                        'and number of frequencies are shown in'
                        'DIN60645-1 ch. 6.1.1. Their order'
                        'are described in ISO8253-1 ch. 6.1')
    parser.add_argument("--results_path", type=str,
                        default='audiometer/results')
    parser.add_argument("--filename", default='result_{}'.format(time.strftime(
                        '%Y-%m-%d_%H-%M-%S')) + '.csv')

    parser.add_argument("--carry_on", type=str)

    parser.add_argument("--logging", type=bool, default=False)

    args = parser.parse_args()

    if not os.path.exists(args.results_path):
        os.makedirs(args.results_path)

    return args


class Controller:

    def __init__(self):

        self.config = config()

        if self.config.carry_on:
            self.csvfile = open(os.path.join(self.config.results_path,
                                             self.config.carry_on), 'r+')
            reader = csv.reader(self.csvfile)
            for row in reader:
                pass
            last_freq = row[1]
            self.config.freqs = self.config.freqs[self.config.freqs.index(
                                                  int(last_freq)) + 1:]
            self.config.earsides[0] = row[2]
            self.writer = csv.writer(self.csvfile)
        else:
            self.csvfile = open(os.path.join(self.config.results_path,
                                             self.config.filename), 'w')
            self.writer = csv.writer(self.csvfile)
            self.writer.writerow(['Level/dB', 'Frequency/Hz', 'Earside'])

        self._audio = tone_generator.AudioStream(self.config.device,
                                                 self.config.attack,
                                                 self.config.release)
        self._rpd = responder.Responder(self.config.timeout,
                                        self.config.responder_device)

    def clicktone(self, freq, level, earside, attack=None, timeout=None,
                fam=False):
        if level >= 0:
            raise OverflowError
        self._audio.start(freq, level, earside, attack=attack)
        click = self._rpd.wait_for_click(timeout=timeout)
        if fam:
            current_level = np.ceil(20 * np.log10(self._audio._last_gain))
            self._audio.stop()
            time.sleep(self.config.timeout + random.random())
            return click, current_level
        self._audio.stop()
        time.sleep(self.config.timeout + random.random())
        return click

    def save_results(self, level, freq, earside):
        row = [level, freq, earside]
        self.writer.writerow(row)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        time.sleep(0.1)
        self._rpd.close()
        self._audio.close()
        self.csvfile.close()

