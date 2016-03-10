"""Generation of pure tones."""

import numpy as np
import sounddevice as sd
import logging

samplerate = 44100


class AudioStream:
    def __init__(self, device, fade_in, fade_out):
        self._stream = sd.OutputStream(device=device,
                                       callback=self._callback, channels=2)
        self._audio_stop = False
        self._inlength = np.round(_seconds_to_samples(fade_in /
                                                      1000)).astype(int)
        self._outlength = np.round(_seconds_to_samples(fade_out /
                                                       1000)).astype(int)
        self._playing = False
        self._running = False
        self._callback_status = sd.CallbackFlags()
        self._stream.start()

    def _callback(self, outdata, frames, time, status):
        self._callback_status |= status
        if self._playing:
            outdata[:] = self._pure_tone(frames, self._freq, self._gain,
                                         self._earside)
            if self._running:
                self._playing = False
        else:
            outdata.fill(0)

    def _pure_tone(self, frames, freq, gain, earside):
        k = np.arange(self._index, self._index + frames) / samplerate
        sine = gain * np.sin(2 * np.pi * freq * k)
        if self._index < self._inlength:  # fade in
            k = k * samplerate / self._inlength
            if self._inlength in k * self._inlength:
                sine[:self._inlength] *= k[:self._inlength]
            else:
                sine *= k
        if self._audio_stop:  # fade out
            k = np.arange(self._outlength) / self._outlength
            k = k[::-1]
            self._end += frames
            if self._end > self._outlength:
                self._end = self._outlength
                #  sine = np.append(sine[:self._end - self._start],
                #                   np.zeros(frames -
                #                   len(sine[:self._end - self._start])))
                sine = np.zeros(frames)
                self._running = True
            else:
                sine *= k[self._start:self._end]
            self._start += frames
        self._index += frames
        sine.shape = -1, 1
        zeros = np.zeros(len(sine))
        zeros.shape = -1, 1
        if earside == 'left':
            sine = np.column_stack((sine, zeros))
        elif earside == 'right':
            sine = np.column_stack((zeros, sine))
        else:
            raise ValueError("'left' or 'right'?")
        return sine

    def start(self, freq, gain_db, earside=None):
        self._freq = freq
        self._gain = _db_to_lin(gain_db)
        self._earside = earside
        self._index = 0
        self._start = 0
        self._end = 0
        self._audio_stop = False
        self._running = False
        self._playing = True

    def stop(self, fade_out):
        self._audio_stop = True
        time.sleep(fade_out/1000)

    def close(self):
        if self._callback_status:
            logging.warning(str(self._callback_status))
        self._stream.stop()


def _seconds_to_samples(seconds):
    return samplerate * seconds


def _db_to_lin(db_value):
    return 10 ** (db_value / 20)
