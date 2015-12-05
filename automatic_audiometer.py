import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import plotting


fs = 44100

test_frequencies = [125, 250, 500, 750, 1000, 1500, 2000, 3000, 4000,
                    6000, 8000]

duration_total = 15 # seconds
duration_sine = 2 # second

intensity_change = 2.5 # dB / sec

t_sine = np.arange(duration_sine * fs) / fs
t_sine.shape = -1,1
t_sine = np.concatenate((t_sine,t_sine),axis=1)
level = 0.001 # 0.001 ^= -60 dB 


y = np.sin(2*np.pi*1000*t_sine) 
sd.play(y, blocking=True, device=0, samplerate=fs, mapping=[1,2])
print(sd.get_status())
print(y.shape)
print(y)



#~ for f in test_frequencies:
    #~ for i in range(duration_total):
        #~ y = level * np.sin(2*np.pi*f*t_sine) 
        #~ sd.play(y, blocking=True)
        #~ level_db = 20 * np.log10(level) + intensity_change
        #~ level = 10 ** (level_db / 20)




