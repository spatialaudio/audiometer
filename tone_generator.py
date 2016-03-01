"""Generation of pure tones."""

import numpy as np
import sounddevice as sd

samplerate = 44100
callback_status = sd.CallbackFlags()


def pure_tone(frames, freq, gain_db, i, timeout, earside):
    packet = i * frames
    k = np.arange(packet) / samplerate
    k_frames = k[packet-frames: packet]
    sine = _db_to_lin(gain_db) * np.sin(2 * np.pi * freq * k_frames)
    if i == 1:
        sine = _fadein(sine, frames)
    if (i+1) * frames > timeout * samplerate:
        sine = _fadeout(sine, frames)
    sine.shape = -1, 1
    zeros = np.zeros(len(sine))
    zeros.shape = -1, 1
    if earside == 'left':
        sine = np.concatenate((sine, zeros), axis=1)
    elif earside == 'right':
        sine = np.concatenate((zeros, sine), axis=1)
    elif earside is None:
        sine = np.concatenate((sine, sine), axis=1)
    else:
        raise NameError("'left' or 'right'?")
    return sine


class AudioStream:
    def __init__(self, device):
        self._stream = sd.OutputStream(device=device,
                                       callback=self._callback, channels=2)
        self._playing = False
        self._stream.start()

    def _callback(self, outdata, frames, time, status):
        global callback_status
        callback_status |= status
        if self._playing:
            outdata[:] = pure_tone(frames, self._freq, self._gain_db,
                                   self._i, self._timeout, self._earside)
            self._i += 1
        else:
            outdata.fill(0)

    def start(self, freq, gain_db, timeout, earside=None):
        self._freq = freq
        self._gain_db = gain_db
        self._i = 1
        self._earside = earside
        self._timeout = timeout
        self._playing = True

    def stop(self):
        self._playing = False

    def close(self):
        self._stream.stop()


def _db_to_lin(db_value):
    return 10 ** (db_value / 20)


def _fadein(sine, frames):
    fade = np.arange(frames) / frames
    sine *= np.power(0.1, (1 - fade) * 5)
    return sine


def _fadeout(sine, frames):
    fade = np.arange(frames) / frames
    sine *= np.power(0.1, (1 - fade) * 5)[::-1]
    return sine
