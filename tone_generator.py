"""Generation of pure tones."""

import numpy as np
import sounddevice as sd

samplerate = 44100
i = 1


playing = False
callback_status = sd.CallbackFlags()


def pure_tone(frames, freq, gain):
    help_var = frames
    global i
    frames = i * frames
    i += 1
    k = np.arange(frames) / samplerate
    k_frames = k[frames-help_var: frames]
    sine = gain * np.sin(2 * np.pi * freq * k_frames)
    sine.shape = -1, 1
    sine = np.concatenate((sine, sine), axis=1)
    return sine


class AudioStream:
    def __init__(self, device):
        self._stream = sd.OutputStream(device=device,
                                       callback=self.callback, channels=2)
        self._freq = 1000
        self._gain = 0.1
        self._stream.start()
     
    def callback(self, outdata, frames, time, status):
        global callback_status
        callback_status |= status
        if playing:
            outdata[:] = pure_tone(frames, self._freq, self._gain)
        else:
            outdata.fill(0)

    def start(self, freq, gain):
        self._freq = freq
        self._gain = gain
        global playing
        playing = True
    
    def stop(self):
        global playing
        playing = False

    def close_stream(self):
        self._stream.stop()



#~ class AudioStream:
    #~ def __init__(self, device):
        #~ def callback(outdata, frames, time, status):
            #~ global callback_status
            #~ callback_status |= status
            #~ if playing:
                #~ outdata[:] = pure_tone(frames, self._freq, self._gain)
            #~ else:
                #~ outdata.fill(0)
        #~ self._stream = sd.OutputStream(device=device, callback=callback, channels=2)
        #~ self._freq = 1000
        #~ self._gain = 0.1
        #~ self._stream.start()
    #~ def start(self, freq, gain):
        #~ self._freq = freq
        #~ self._gain = gain
        #~ global playing
        #~ playing = True
    #~ def stop(self):
        #~ global playing
        #~ playing = False
    #~ def close_stream(self):
        #~ self._stream.stop()



 #~ 
#~ with responder.MouseResponder():
    #~ with sd.OutputStream(device=0, callback=callback): 
        #~ sd.sleep(dur * 1000)
