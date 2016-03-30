"""Generation of pure tones."""

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import logging
import time

samplerate = 44100


class AudioStream:
    def __init__(self, device, fade_in, fade_out):
        self._stream = sd.OutputStream(device=device,
                                       callback=self._callback, channels=2)
        self._inlength = np.round(_seconds_to_samples(fade_in /
                                                      1000)).astype(int)
        self._outlength = np.round(_seconds_to_samples(fade_out /
                                                       1000)).astype(int)
        self._gain = 0
        self._target_gain = 0
        self._weight_gain = 0
        self._last_gain = 0
        self._freq = 0
        self._channel = 0
        self._index = 0
        self._total_output = []
        self._callback_status = sd.CallbackFlags()
        self._stream.start()

    def _callback(self, outdata, frames, time, status):
        self._callback_status |= status
        # self._callback_status.output_overflow = True
        outdata.fill(0)
        k = np.arange(self._index, self._index + frames)
        if self._target_gain >= self._last_gain:  # fade in
            self._gain = np.minimum(self._target_gain, self._weight_gain *
                                    k / self._inlength)
        else:  # fade out
            self._start = self._start - frames
            self._gain = np.maximum(self._target_gain, self._weight_gain *
                                    np.arange(self._start, self._end)[::-1] /
                                    self._outlength)
            self._end = self._end - frames
        outdata[:, self._channel] = self._gain * np.sin(2 * np.pi *
                                                        self._freq *
                                                        k / samplerate)
        self._index += frames
        self._last_gain = self._gain[-1]
        self._total_output = np.hstack((self._total_output,
                                        outdata[:, self._channel]))

    def start(self, freq, gain_db, earside=None):
        self._freq = freq
        self._target_gain = _db2lin(gain_db)
        self._weight_gain = _db2lin(gain_db)
        self._last_gain = 0
        self._index = 0
        if earside == 'left':
            self._channel = 1
        elif earside == 'right':
            self._channel = 0
        else:
            raise ValueError("'left' or 'right'?")

    def stop(self):
        self._target_gain = 0
        self._start = self._outlength
        self._end = self._outlength
        while(self._last_gain != 0):
            # pass
            time.sleep(0.1)

    def close(self):
        if self._callback_status:
            logging.warning(str(self._callback_status))
        self._stream.stop()

    def plotting_output(self):
        plt.plot(np.arange(len(self._total_output)) /
                 samplerate, self._total_output)
        plt.show()


def _seconds_to_samples(seconds):
    return samplerate * seconds


def _db2lin(db_value):
    return 10 ** (db_value / 20)
