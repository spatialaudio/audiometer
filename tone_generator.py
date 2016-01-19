"""Generation of pure tones."""

import numpy as np
import sounddevice as sd

samplerate = 44100
globgain = 1
globfreq = 1000
i = 1


playing = False

callback_status = sd.CallbackFlags()

def callback(outdata, frames, time, status):
    global callback_status
    callback_status |= status
    if playing:
        outdata[:] = pure_tone(frames)
    else:
        outdata.fill(0)

 
def pure_tone(frames):
    help_var = frames
    global i 
    frames = i * frames
    i += 1 
    k = np.arange(frames) / samplerate
    k_frames = k[frames-help_var: frames]
    sine = globgain * np.sin(2 * np.pi * globfreq * k_frames)
    sine.shape = -1, 1
    sine = np.concatenate((sine, sine), axis=1)
    return sine
    


class AudioStream:
    def __init__(self, device):
        self._stream = sd.OutputStream(device=device, callback=callback, channels=2)
        self._stream.start()
    def start(self, freq, gain):
        global globfreq
        globfreq = freq
        global globgain
        globgain = gain
        global playing
        playing = True
    def stop(self):
        global playing
        playing = False
    def close_stream(self):
        self._stream.stop()
    
    
    
 #~ 
#~ with responder.MouseResponder():
    #~ with sd.OutputStream(device=0, callback=callback): 
        #~ sd.sleep(dur * 1000)
