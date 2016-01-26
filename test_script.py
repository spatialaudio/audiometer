import tone_generator
import time
import responder

device = 0

audio = tone_generator.AudioStream(device) 
res = responder.MouseResponder()
audio.start(1000,0.1)
print("waiting")
res.wait_for_click() # blocking function
print("Received click")
audio.stop()
res.stop()

time.sleep(2)

res = responder.MouseResponder()
audio.start(10000,0.5)
print("waiting")
res.wait_for_click() # blocking function
res.stop()
audio.stop()
