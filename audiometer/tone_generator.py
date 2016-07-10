"""Generation of pure tones."""

import numpy as np
import sounddevice as sd
import logging

samplerate = 44100


class AudioStream:
    def __init__(self, device, attack, release):
        if attack <= 0 or release <= 0:
            raise ValueError("attack and release have to be positive "
                             "and different from zero")
        self._stream = sd.OutputStream(device=device,
                                       callback=self._callback, channels=2)
        self._attack = np.round(_seconds2samples(attack / 1000)).astype(int)
        self._release = np.round(_seconds2samples(release / 1000)).astype(int)
        self._last_gain = 0
        self._channel = 0
        self._index = 0
        target_gain = 0
        slope = 0
        freq = 0
        self._callback_parameters = target_gain, slope, freq
        self._target_gain = target_gain
        self._callback_status = sd.CallbackFlags()
        self._stream.start()

    def _callback(self, outdata, frames, time, status):
        assert frames > 0
        self._callback_status |= status
        # This is thread-safe, see http://stackoverflow.com/a/17881014/500098:
        target_gain, slope, freq = self._callback_parameters
        outdata.fill(0)
        k = np.arange(self._index, self._index + frames)
        ramp = np.arange(frames) * slope + self._last_gain + slope
        assert slope != 0 or (target_gain == 0 and self._last_gain == 0)
        if slope > 0:
            gain = np.minimum(target_gain, ramp)
        else:
            gain = np.maximum(target_gain, ramp)
        signal = gain * np.sin(2 * np.pi * freq * k / samplerate)
        outdata[:, self._channel] = signal
        self._index += frames
        self._last_gain = gain[-1]

    def start(self, freq, gain_db, earside=None):
        if self._target_gain != 0:
            raise ValueError("Before calling start(), "
                             "target_gain must be zero")
        if gain_db == -np.inf:
            raise ValueError("gain_db must be a finite value")
        target_gain = _db2lin(gain_db)
        slope = target_gain / self._attack
        self._target_gain = target_gain
        self._freq = freq
        self._callback_parameters = target_gain, slope, freq
        if earside == 'left':
            self._channel = 0
        elif earside == 'right':
            self._channel = 1
        else:
            raise ValueError("'left' or 'right'?")

    def stop(self):
        if self._target_gain == 0:
            raise ValueError("Before calling stop(),"
                             "target_gain must be different from zero")
        target_gain = 0
        slope = - self._target_gain / self._release
        self._target_gain = target_gain
        self._callback_parameters = target_gain, slope, self._freq

    def close(self):

        if self._callback_status:
            logging.warning(str(self._callback_status))
        self._stream.stop()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def _db2lin(db_value):
    return 10 ** (db_value / 20)


def _seconds2samples(seconds):
    return samplerate * seconds
