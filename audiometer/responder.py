"""The responder module processes the reaction to acoustic signals."""

from .pyxhook import pyxhook
import threading
import time


class MouseResponder:

    def __init__(self):
        self._event = threading.Event()
        self._event.set()
        self._hookman = pyxhook.HookManager()
        self._hookman.MouseAllButtonsDown = self._mcevent
        self._hookman.start()

    def close(self):
        time.sleep(0.01)
        self._hookman.cancel()

    def wait_for_click(self, timeout=None):
        self._event.clear()
        self._event.wait(timeout=timeout)
        return self._event.is_set()

    def _mcevent(self, event):
        if event.MessageName == "mouse left down":
            self._event.set()

    def __exit__(self, *args):
        self.close()

    def __enter__(self):
        return self
