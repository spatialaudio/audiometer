"""The responder module processes the reaction to acoustic signals."""

from .pyxhook import pyxhook
import threading
import os
import time


class Responder:

    def __init__(self, tone_duration):
        os.system("stty -echo")
        self._timeout = tone_duration
        self._event1 = threading.Event()
        self._event1.set()
        self._event2 = threading.Event()
        self._event2.set()
        self._event3 = threading.Event()
        self._event3.set()
        self._hookman = pyxhook.HookManager()
        self._hookman.MouseAllButtonsDown = self._mcevent_down
        self._hookman.MouseAllButtonsUp = self._mcevent_up
        self._hookman.KeyDown = self._kbevent
        self._hookman.start()

    def close(self):
        time.sleep(0.01)
        self._hookman.cancel()

    def click_down(self):
        if self._event1.is_set() and not self._event3.is_set():
            return True
        else:
            return False

    def click_up(self):
        if self._event3.is_set():
            return True
        else:
            return False

    def clear(self):
        self._event1.clear()
        self._event2.clear()
        self._event3.clear()

    def wait_for_arrow(self):
        self._event2.clear()
        self._event2.wait()
        return self._key

    def wait_for_click_up(self):
        self._event3.wait()

    def wait_for_click_down_and_up(self):
        self._event1.wait()
        self._event3.wait()

    def _mcevent_down(self, event):
        if event.MessageName == "mouse left down":
            self._event1.set()
            self._event3.clear()

    def _mcevent_up(self, event):
        if event.MessageName == "mouse left up":
            self._event3.set()

    def _kbevent(self, event):
        if event.MessageName == "key down" and event.Key == "Left":
            self._key = "arrow_left"
            self._event2.set()
        if event.MessageName == "key down" and event.Key == "Right":
            self._key = "arrow_right"
            self._event2.set()
        if event.MessageName == "key down" and event.Key == "space":
            self._key = "space"
            self._event2.set()

    def __exit__(self, *args):
        os.system("stty echo")
        self.close()

    def __enter__(self):
        return self
