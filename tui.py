import curses

class Screen:
    def __init__(self,win):
        self.win = win
        self.max_y,self.max_x = win.getmaxyx()

    def clear(self):
        self.win.clear()
        self.win.refresh()

    def print(self ,row=0, col=0 , msg = "",color = curses.COLOR_WHITE):
        if row >= self.max_y or col >= self.max_x:
            return
        self.win.addstr(row, col, msg, color)

class Dialog(Screen):

    def __init__(self, win):
        super().__init__(win)
        win.border()
    
    def print_dialog(self, cur_text, target):
        cur_row = 1
        cur_col = 1
        max_col = 0
        for i, char in enumerate(target):
            
            if char == "\n" :
                cur_col = 1
                cur_row += 1
                continue
           
            if cur_row + 10 >= self.max_y:
                break
           
            self.print(cur_row, cur_col, char)
            cur_col += 1

            if cur_col > max_col:
                 max_col = cur_col

        self.max_col = max_col
        self.max_row = cur_row
        cur_row = 1
        cur_col = 1
        
        for i, char in enumerate(cur_text):
            correct_char = target[i]
            color = curses.color_pair(1)
            
            if char == "\n":
                cur_col = 0
                cur_row += 1
                continue

            if char != correct_char:
                color=curses.color_pair(2)
                char = correct_char

            self.print(cur_row, cur_col, char, color)
            cur_col += 1


        if cur_text and target[len(cur_text) - 1] == "\n":
            
            if cur_text[-1] != "\n":
                cur_text.pop()
            
            else:
                y, x = self.win.getyx()
                self.win.move(y+1, 0)

class Status(Screen):
    def __init__(self, win):
        super().__init__(win)

class AuthorWin(Screen):
    def __init__(self, win):
        super().__init__(win)

    def print(self, author = "",color = curses.COLOR_WHITE):
        author = "-- "+author
        col = self.max_x - len(author)
        if col < 0:
            col = 0
        self.win.addstr(0, col, author, color)


