"""The responder module processes the reaction to acoustic signals."""

import curses
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
            return True
        return False 

    def close(self):
        curses.endwin()
