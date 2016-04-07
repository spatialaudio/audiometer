"""Generation of pure tones."""

import numpy as np
import sounddevice as sd
import logging

samplerate = 44100


class AudioStream:
    def __init__(self, device, attack, release):
        self._stream = sd.OutputStream(device=device,
                                       callback=self._callback, channels=2)
        self._attack = np.round(_seconds2samples(attack / 1000)).astype(int)
        self._release = np.round(_seconds2samples(release / 1000)).astype(int)
        self._gain = 0
        self._slope = 0
        self._target_gain = 0
        self._last_gain = 0
        self._freq = 0
        self._channel = 0
        self._index = 0
        self._callback_status = sd.CallbackFlags()
        self._stream.start()

    def _callback(self, outdata, frames, time, status):
        self._callback_status |= status
        outdata.fill(0)
        k = np.arange(self._index, self._index + frames)
        ramp = np.arange(frames) * self._slope + self._last_gain + self._slope
        if self._target_gain >= self._last_gain:
            self._gain = np.minimum(self._target_gain, np.absolute(ramp))
        else:
            self._gain = np.maximum(self._target_gain, ramp)
        signal = self._gain * np.sin(2 * np.pi * self._freq * k / samplerate)
        outdata[:, self._channel] = signal
        self._index += frames
        self._last_gain = self._gain[-1]

    def start(self, freq, gain_db, earside=None):
        self._freq = freq
        self._target_gain = _db2lin(gain_db)
        self._slope = self._target_gain / self._attack
        self._index = 0
        if earside == 'left':
            self._channel = 1
        elif earside == 'right':
            self._channel = 0
        else:
            raise ValueError("'left' or 'right'?")

    def stop(self):
        self._slope = - self._target_gain / self._release
        self._target_gain = 0

    def close(self):
        if self._callback_status:
            logging.warning(str(self._callback_status))
        self._stream.stop()


def _seconds2samples(seconds):
    return samplerate * seconds


def _db2lin(db_value):
    return 10 ** (db_value / 20)
