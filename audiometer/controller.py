from audiometer import tone_generator
from audiometer import responder
import numpy as np
import argparse
import time
import os
import csv
import random


def config():

    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument(
        "--device", help='How to select your soundcard is '
        'shown in http://python-sounddevice.readthedocs.org/en/0.3.3/'
        '#sounddevice.query_devices', type=int, default=None)
    parser.add_argument("--beginning-fam-level", type=float, default=40,
                        help="in dBHL")
    parser.add_argument("--attack", type=float, default=30)
    parser.add_argument("--release", type=float, default=40)
    parser.add_argument(
        "--tone-duration", type=float, default=2, help='For more'
        'information on the tone duration have a look at '
        'ISO8253-1 ch. 6.2.1')
    parser.add_argument("--tolerance", type=float, default=1.5)
    parser.add_argument(
        "--pause-time", type=float, default=[2, 3], nargs=2, help="The pause "
        "time is calculated by an interval [a,b] randomly. It represents "
        "the total duration after the tone presentation. Please note, "
        "the pause time has to be greater than or equal to the tone duration")
    parser.add_argument("--earsides", type=str, nargs='+',
                        default=['right', 'left'], help="The first list item "
                        "represents the beginning earside. The second list "
                        "item represents the ending earside, consequently. "
                        "It is also possible to choose only one earside, "
                        "left or right")
    parser.add_argument("--small-level-increment", type=float, default=5)
    parser.add_argument("--large-level-increment", type=float, default=10)
    parser.add_argument("--small-level-decrement", type=float, default=10)
    parser.add_argument("--large-level-decrement", type=float, default=20)
    parser.add_argument("--start-level-familiar", type=float, default=-40)
    parser.add_argument("--freqs", type=float, nargs='+', default=[1000, 1500,
                        2000, 3000, 4000, 6000, 8000, 750, 500, 250, 125],
                        help='The size '
                        'and number of frequencies are shown in'
                        'DIN60645-1 ch. 6.1.1. Their order'
                        'are described in ISO8253-1 ch. 6.1')
    parser.add_argument("--conduction", type=str, default='air', help="How "
                        "do you connect the headphones to the head? Choose "
                        " air or bone.")
    parser.add_argument("--masking", default='off')
    parser.add_argument("--results-path", type=str,
                        default='audiometer/results/')
    parser.add_argument("--filename", default='result_{}'.format(time.strftime(
                        '%Y-%m-%d_%H-%M-%S')) + '.csv')

    parser.add_argument("--carry-on", type=str)
    parser.add_argument("--logging", action='store_true')
    # Calibration for my SoundCard: Intel Corporation 6 Series/C200 Series
    # Chipset Family High Definition Audio Controller
    # PC Sound Level: Maximum
    # Calibration values: [frequency, reference, correction]
    parser.add_argument("--cal125", default=[125, -81, 17])
    parser.add_argument("--cal250", default=[250, -92, 12])
    parser.add_argument("--cal500", default=[500, -80, -5])
    parser.add_argument("--cal750", default=[750, -85, -3])
    parser.add_argument("--cal1000", default=[1000, -84, -4])
    parser.add_argument("--cal1500", default=[1500, -82, -4])
    parser.add_argument("--cal2000", default=[2000, -90, 2])
    parser.add_argument("--cal3000", default=[3000, -94, 10])
    parser.add_argument("--cal4000", default=[4000, -91, 11])
    parser.add_argument("--cal6000", default=[6000, -70, -5])
    parser.add_argument("--cal8000", default=[8000, -76, 1])

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
            self.writer.writerow(['Conduction', self.config.conduction, None])
            self.writer.writerow(['Masking', self.config.masking, None])
            self.writer.writerow(['Level/dB', 'Frequency/Hz', 'Earside'])

        self.cal_parameters = np.vstack((self.config.cal125,
                                        self.config.cal250,
                                        self.config.cal500,
                                        self.config.cal750,
                                        self.config.cal1000,
                                        self.config.cal1500,
                                        self.config.cal2000,
                                        self.config.cal3000,
                                        self.config.cal4000,
                                        self.config.cal6000,
                                        self.config.cal8000))

        self._audio = tone_generator.AudioStream(self.config.device,
                                                 self.config.attack,
                                                 self.config.release)
        self._rpd = responder.Responder(self.config.tone_duration)

    def clicktone(self, freq, current_level_dBHL, earside):
        if self.dBHL2dBFS(freq, current_level_dBHL) > 0:
            raise OverflowError
        self._rpd.clear()
        self._audio.start(freq, self.dBHL2dBFS(freq, current_level_dBHL),
                          earside)
        time.sleep(self.config.tone_duration)
        click_down = self._rpd.click_down()
        self._audio.stop()
        if click_down:
            start = time.time()
            self._rpd.wait_for_click_up()
            end = time.time()
            if (end - start) <= self.config.tolerance:
                time.sleep(random.uniform(self.config.pause_time[0],
                           self.config.pause_time[1]))
                return True
            else:
                time.sleep(random.uniform(self.config.pause_time[0],
                           self.config.pause_time[1]))
                return False

        else:
            time.sleep(random.uniform(self.config.pause_time[0],
                                      self.config.pause_time[1]))
            return False

    def audibletone(self, freq, current_level_dBHL, earside):
        self.key = ''
        while self.key != 'space':
            if self.dBHL2dBFS(freq, current_level_dBHL) > 0:
                print("WARNING: Signal is distorted. Decrease the current "
                      "level!")
            self._audio.start(freq,
                              self.dBHL2dBFS(freq, current_level_dBHL),
                              earside)
            self.key = self._rpd.wait_for_arrow()
            if self.key == 'arrow_left':
                current_level_dBHL -= 5
            if self.key == 'arrow_right':
                current_level_dBHL += 5
            self._audio.stop()

        return current_level_dBHL

    def wait_for_click(self):
        self._rpd.clear()
        self._rpd.wait_for_click_down_and_up()
        time.sleep(1)

    def save_results(self, level, freq, earside):
        row = [level, freq, earside]
        self.writer.writerow(row)

    def dBHL2dBFS(self, freq_value, dBHL):
        calibration = [(ref, corr) for freq, ref, corr in self.cal_parameters
                       if freq == freq_value]
        return calibration[0][0] + calibration[0][1] + dBHL

    def __enter__(self):
        return self

    def __exit__(self, *args):
        time.sleep(0.1)
        self._rpd.__exit__()
        self._audio.close()
        self.csvfile.close()
