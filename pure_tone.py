"""Pure tone generation by a Callback-Function."""

import numpy as np
import sounddevice as sd

fs = 44100
dur = 3  # seconds
i = 1


def pure_tone(amp, dur, freq, samplerate, frames, **kwargs):
    help_var = frames
    global i
    frames = i * frames
    i += 1
    t = np.arange(dur * samplerate) / samplerate
    t_frames = t[frames-help_var: frames]
    sine = amp * np.sin(2 * np.pi * freq * t_frames)
    sine.shape = -1, 1
    sine = np.concatenate((sine, sine), axis=1)  # stereo
    if(frames > len(t)):  # fill up the last frames with zeros
        sine = np.concatenate((sine, np.zeros((frames-len(t), 2))))
    return sine


def get_chunk(frames):
    chunk = pure_tone(amp=1.0, dur=dur, freq=1000, samplerate=fs,
                      frames=frames)
    return chunk

callback_status = sd.CallbackFlags()


def callback(outdata, frames, time, status):
    global callback_status
    callback_status |= status
    outdata[:] = get_chunk(frames)

with sd.OutputStream(samplerate=fs, callback=callback):
    sd.sleep(dur * 1000)
