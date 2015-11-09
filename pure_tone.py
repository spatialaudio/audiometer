import numpy as np
import sounddevice as sd

fs = 44100
dur = 5  # seconds


def pure_tone(amp, dur, freq, phase, samplerate, **kwargs):
    t = np.arange(dur * samplerate) / samplerate
    sine = amp * np.sin(2 * np.pi * freq * t + phase)
    return sine


def get_chunk():
    data = pure_tone(amp=1.0, dur=dur, freq=1000, phase=0, samplerate=fs)
    return data

callback_status = sd.CallbackFlags()


def callback(indata, frames, time, status):
    global callback_status
    callback_satus |= status
    chunk = get_chunk()
    return chunk

stream = sd.Stream(samplerate=fs, callback=callback)
sd.sleep(dur * 1000)
