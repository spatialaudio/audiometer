import tone_generator
import time
import responder


device = 0
timeout = 2  # seconds

audio = tone_generator.AudioStream(device)  # open stream
rpd = responder.MouseResponder()  # initialize MouseResponder
audio.start(500, -30, timeout, earside='right')  # start first tone
print("wait for clicking1")
click = rpd.wait_for_click(timeout)  # you have 2 seconds to click

audio.stop()  # stop tone
rpd.close()  # close responder
rpd = responder.MouseResponder()  # reinitialize MouseResponder

if click:  # if tone is audible (clicking)..increase next tone
    audio.start(3000, -26, timeout, earside='left')  # start increased tone
    print("wait for clicking2")
    click = rpd.wait_for_click(timeout)
    audio.stop()
    rpd.close()

else:  # if tone is not audible (not clicking)...decrease next tone
    audio.start(1000, -40, timeout, earside='left')
    print("wait for clicking3")
    click = rpd.wait_for_click(timeout)
    audio.stop()
    rpd.close()

audio.close()
