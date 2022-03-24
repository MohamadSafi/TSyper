import curses
from curses import wrapper
import time
import json
import random
import sys
import logging
from tui import Screen, Dialog, Status, AuthorWin
    
logging.basicConfig(filename = "TST.log", filemode = "w", format = "[%(levelname)s] - %(asctime)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

KEY_ESC = 27
KEY_TAB = 9
EXIT = 0
NEW_QUOTE = 2

MIN_TERM_WIDTH = 100
MIN_TERM_HEIGHT = 5

PADDING = 1
DIALOG_HEIGHT = 19 
AUTHOR_WIN_HEIGHT = 2
AUTHOR_WIN_BEGIN = DIALOG_HEIGHT + PADDING
STATUS_HEIGHT = 2
STATUS_BEGIN = AUTHOR_WIN_BEGIN + PADDING
WIN_WIDTH = 100


class Tsyper:
    def __init__(self, stdscr):
        if len(sys.argv) > 1:
            quote_type = sys.argv[1]
        else:
            quote_type = "short"

        self.win = stdscr
        self.max_y,self.max_x = self.win.getmaxyx()
        curses.use_default_colors()
        curses.curs_set(0)
        curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK,curses.COLOR_RED)
        curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
        curses.init_pair(4,curses.COLOR_YELLOW,-1)
        
        if self.max_x < MIN_TERM_WIDTH or self.max_y < MIN_TERM_HEIGHT:
            self.win.addstr(0,0,"Open a bigger terminal Please", curses.color_pair(2) )
            self.win.nodelay(False)
            self.win.getkey()
            return 

        logger.debug("max_x = {} , max_y = {}".format(self.max_x,self.max_y))
        self.dialog = Dialog(self.win.subwin(DIALOG_HEIGHT,WIN_WIDTH,0,0))
        self.author_win = AuthorWin(self.win.subwin(AUTHOR_WIN_HEIGHT,WIN_WIDTH,AUTHOR_WIN_BEGIN,0))
        self.statusbar = Status(self.win.subwin(STATUS_HEIGHT,WIN_WIDTH,STATUS_BEGIN,0))

        while True:
            quote = self.get_random_quote(quote_type)
            test_res = self.wpm_test(quote)

            if test_res  == EXIT:
                break
            elif test_res == NEW_QUOTE:
                self.author_win.clear()
                self.dialog.clear()
                continue

            self.statusbar.print(msg = f"You completed the text! your WPM is {wpm} | Press Enter to try again...")
            self.win.nodelay(False)
            key = self.win.getkey()
            self.dialog.clear()

    def load_quotes(self):
        with open("quotes.json","r") as file:
            quotes = json.load(file)
        return quotes


    def get_random_quote(self, quote_type="short"):
        quotes = self.load_quotes()
        quotes = quotes[quote_type]
        return random.choice(quotes)


    def wpm_test(self, quote):
        target = quote[0]
        author = quote[1]
        current = []
        global wpm
        wpm = 0
        start_time = time.time()
        start_timer = False

        while True:
            if start_timer:
                time_elapsed = max(time.time() - start_time, 1)
                wpm = round((len(current) / (time_elapsed /60)) / 5)
            else:
                time_elapsed = 0

            self.dialog.print_dialog(current, target,curses.color_pair(1),curses.color_pair(2))
            self.author_win.print(author = author)
            self.statusbar.print(msg = "WPM:{}".format(wpm))

            if not current:
                msg = "Press TAB to change the text, ESC to Exit or Any key to start typing"
                self.statusbar.print(msg = msg)

            if "".join(current) == target:
                return True

            try:
                key = self.win.getkey()
                logger.debug("{} has been pressed".format(key))
                start_timer = True

            except Exception:
                raise

            try:
                if ord(key) == KEY_ESC:
                    return EXIT
                if ord(key) == KEY_TAB:
                    return NEW_QUOTE
            except:
                if key not in ("KEY_BACKSPACE", "\b", "\x7f"):
                    continue

            if key in ("KEY_BACKSPACE", "\b", "\x7f"):
                if len(current) > 0:
                    current.pop()
            elif len(current) < len(target):
                if (current and key == "\n") and ((current[-1] == key) or (target[len(current)] != key) or (not current and key == "\n")):
                    continue
                else:
                    current.append(key)
                    logger.debug(current)
if __name__ == "__main__":
    curses.wrapper(Tsyper)
