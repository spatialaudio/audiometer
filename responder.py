"""The responder module processes the reaction to acoustic signals."""

import curses
import pyxhook
import time


class MouseResponder:

    def __init__(self):

        self._stdscr = curses.initscr()
        self._stdscr.refresh()
        self._stdscr.keypad(True)
        curses.mousemask(True)

    def wait_for_click(self, timeout=None):
        if timeout is not None:
            curses.halfdelay(10 * timeout)
        event = self._stdscr.getch()
        if event == curses.KEY_MOUSE:
            return True  # clicking returns True, not clicking None

    def close(self):
        curses.endwin()


#  def kbevent(event):
#    print(event)

#  class MouseResponder:
#    def __enter__(self):
#        return self
#    def __exit__(self,*arg):
#        self.hookman.cancel()
#    def __init__(self):
#        self.hookman = pyxhook.HookManager()
#        self.hookman.MouseAllButtonsDown = kbevent
#        self.hookman.start()
