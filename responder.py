"""The responder module processes the reaction to acoustic signals."""

import curses 
import pyxhook

    
class MouseResponder:

    def __init__(self):

        self._screen = curses.initscr() 
        self._screen.refresh()
        self._screen.keypad(True) 
        curses.mousemask(True)
    
    def wait_for_click(self):
        event = self._screen.getch() 
    
    def stop(self):
        curses.endwin()



#~ def kbevent(event):
    #~ print(event)
#~ 
#~ class MouseResponder:
    #~ def __enter__(self):
        #~ return self
    #~ def __exit__(self,*arg):
        #~ self.hookman.cancel()
    #~ def __init__(self):
        #~ self.hookman = pyxhook.HookManager()
        #~ self.hookman.MouseAllButtonsDown = kbevent
        #~ self.hookman.start()
    
    

