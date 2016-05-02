from audiometer import tone_generator
from audiometer import responder
from configparser import ConfigParser
import time
import random


class Controller:

    def __init__(self):
        self._cfg1 = ConfigParser()
        self._cfg2 = ConfigParser()
        self._cfg1.read('config.ini')
        device = int(self._cfg1['Device']['device'])
        attack = int(self._cfg1['FadeIn/FadeOut Time']['attack'])
        release = int(self._cfg1['FadeIn/FadeOut Time']['release'])
        self._timeout = int(self._cfg1['Timeout']['timeout'])
        responder_device = self._cfg1['Responder']['responder_device']

        self._audio = tone_generator.AudioStream(device, attack, release)
        self._rpd = responder.Responder(self._timeout, responder_device)

    def _freq_list(self):
        # http://stackoverflow.com/a/30223001
        str_freqs = self._cfg1.get('Standard Frequencies', 'freqs').split('\n')
        freq_list = [int(i) for i in str_freqs]
        return (freq_list[freq_list.index(1000):] +
        freq_list[:freq_list.index(1000)][::-1])

    def _earside(self):
        earside_beginning = self._cfg1['Beginning Earside']['earside']
        if earside_beginning == 'right':
            earside_contralateral = 'left'
        elif earside_beginning == 'left':
            earside_contralateral = 'right'
        else:
            raise ValueError("earside_beginning must be 'right' or 'left'")
        return earside_beginning, earside_contralateral

    def _process(self, freq, level, earside):
        if level >= 0:
            raise OverflowError("The signal is distorted. Please, repeat "
            "the hearing test")
        self._audio.start(freq, level, earside)
        click = self._rpd.wait_for_click()
        self._audio.stop()
        time.sleep(self._timeout + random.random())  # described in chapter 3.1
        return click

    def _save_results(self, level, freq, earside, section):
        self._cfg2.read('results.ini')
        if section not in self._cfg2:
            self._cfg2.add_section(section)
        self._cfg2.set(section, 'level_{}Hz_{}'.format(freq, earside),
            str(level))
        with open('results.ini', 'w') as self._res:
            self._cfg2.write(self._res)

    def _exit(self):
        time.sleep(0.1)
        self._rpd.close()
        self._audio.close()

