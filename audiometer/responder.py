"""The responder module processes the reaction to acoustic signals."""

from .pyxhook import pyxhook
import threading
import time


class Responder:

    def __init__(self, timeout, responder_device):
        self._timeout = timeout
        self._event = threading.Event()
        self._event.set()
        self._hookman = pyxhook.HookManager()
        if responder_device == "mouse left":
            self._hookman.MouseAllButtonsDown = self._mcevent
        elif responder_device == 'spacebar':
            self._hookman.KeyDown = self._kbevent
        else:
            raise ValueError("The string ist not valid")
        self._hookman.start()

    def close(self):
        time.sleep(0.01)
        self._hookman.cancel()

    def wait_for_click(self, timeout=None):
        self._event.clear()
        if timeout is None:
            self._event.wait(timeout=self._timeout)
        else:
            self._event.wait(timeout=timeout)

        return self._event.is_set()

    def _mcevent(self, event):
        if event.MessageName == "mouse left down":
            self._event.set()

    def _kbevent(self, event):
        if event.MessageName == "key down" and event.Key == "space":
            self._event.set()

    def __exit__(self, *args):
        self.close()

    def __enter__(self):
        return self
