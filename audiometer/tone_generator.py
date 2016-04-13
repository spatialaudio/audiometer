"""Generation of pure tones."""

import numpy as np
import sounddevice as sd
import logging

samplerate = 44100


class AudioStream:
    def __init__(self, device, attack, release):
        assert attack > 0 and release > 0, (
            "attack and release have to be positive and different from zero")
        self._stream = sd.OutputStream(device=device,
                                       callback=self._callback, channels=2)
        self._attack = np.round(_seconds2samples(attack / 1000)).astype(int)
        self._release = np.round(_seconds2samples(release / 1000)).astype(int)
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
        mytuple = self._slope, self._target_gain
        # This is thread-safe, see http://stackoverflow.com/a/17881014/500098:
        slope, target_gain = mytuple
        outdata.fill(0)
        k = np.arange(self._index, self._index + frames)
        ramp = np.arange(frames) * slope + self._last_gain + slope
        if slope > 0:
            gain = np.minimum(target_gain, ramp)
        else:
            gain = np.maximum(target_gain, ramp)
        signal = gain * np.sin(2 * np.pi * self._freq * k / samplerate)
        outdata[:, self._channel] = signal
        self._index += frames
        self._last_gain = gain[-1]

    def start(self, freq, gain_db, earside=None):
        assert self._target_gain == 0, (
            "Before calling start(), target_gain has to be zero")
        assert gain_db != -np.inf, "gain_db has to be a finite value"
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
        assert self._target_gain != 0, (
            "Before calling stop(), target_gain has to be different from zero")
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
