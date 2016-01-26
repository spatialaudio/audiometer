import tone_generator
import time
import responder


device = 0
duration = 2 # duration of tone in seconds

audio = tone_generator.AudioStream(device)  # open stream
rpd = responder.MouseResponder()  # initialize MouseResponder
audio.start(1000, 0.03)  # start first tone
print("wait for clicking1")
click = rpd.wait_for_click(duration)  # you have 2 seconds to click 

audio.stop()  # stop tone
rpd.stop()  # stop responder
rpd = responder.MouseResponder()  # reinitialize MouseResponder

if click is True:  # if tone is audible (clicking)..increase next tone
    audio.start(1000, 0.05)  # start increased tone
    print("wait for clicking2")
    click = rpd.wait_for_click(duration)
    audio.stop()
    rpd.stop()

else:  # if tone is not audible (not clicking)...decrease next tone
    audio.start(1000, 0.01)
    print("wait for clicking3")
    click = rpd.wait_for_click(duration)
    audio.stop()
    rpd.stop()
