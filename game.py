import tkinter as tk 
import random 
import time 
from math import log
import numpy as np

class Game(tk.Tk):
    board = []
    score = 0 
    high_score = 0 
    score_string = high_score_string = None
    CANVAS_WIDTH = 600
    CANVAS_HIGHT = 600


    print_fills = [
        'f5f5f5',
        'e0f2f8',
        'b8dbe5',
        '71b1bd',
        '27819f',
        '0073b9',
        '7fa8d7',
        '615ea6',
        '2f3490',
        '1c1862',
        '9c005d',
        'c80048'
    ]



    def __init__(self, N, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.score_string = tk.StringVar(self)
        self.high_score_string = tk.StringVar(self)
        self.score_string.set("0")
        self.N = N


        self.create_widgets()
        self.canvas = tk.Canvas(self, width=self.CANVAS_WIDTH, height=self.CANVAS_HIGHT, borderwidth=5, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="false")
        self.new_game()
    
    def new_game(self):
        self.score = 0
        self.score_string.set("0")

        self.board = np.zeros((self.N, self.N))
        
        i = 0 
        while i < random.randint(2, 3):
            x = random.randint(0, self.N-1)
            y = random.randint(0, self.N-1)
            
            if self.board[x, y] == 0:
                self.board[x, y] = random.choice([2, 2, 2, 4]) #Making the odds of getting 4 at starting as 25%
                i += 1 
        
        self.print_board()

    def print_board(self):
        self.cell_width = self.CANVAS_WIDTH//self.N
        self.cell_height = self.CANVAS_HIGHT//self.N
        self.score_string.set(str(self.score))

        self.square = {}

        for row in range(self.N):
            for column in range(self.N):

                x1 = column*self.cell_width
                y1 = row*self.cell_height
                x2 = x1+self.cell_width - 5
                y2 = y1+self.cell_height - 5

                num = self.board[row, column]
                self.print_num(num, row, column, x1, y1, x2, y2)

    def print_num(self, num, row, column, x1, y1, x2, y2):

        if num == 0:
            self.square[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#"+self.print_fills[0], tags="rect", outline="")
        else:
            self.square[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#"+self.print_fills[int(log(num, 2))%len(self.print_fills)], tags="rect", outline="")
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, font=("Arial", 32), fill="black", text=str(num))

    def create_widgets(self):
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=2, column=0, columnspan=self.N)
        tk.Button(self.button_frame, text="New Game", command=self.new_game).grid(row=0, column=0)
        tk.Label(self.button_frame, text="Score: ").grid(row=0, column=1)
        tk.Label(self.button_frame, textvariable=self.score_string).grid(row=0, column=2)
        #tk.Label(self.button_frame, text="Record: ").grid(row=0, column=3)
        tk.Label(self.button_frame, textvariable=self.high_score_string).grid(row=0, column=4)
        self.button_frame.pack(side="top")


    def is_filled(self):
        for i in range(self.N):
            if 0 in self.board[i]:
                return False 
        return True


    def add_new_tile(self):
        if not self.is_filled():
            x, y = random.choice(self.empty_indices())
            self.board[x, y] = random.choice([2, 2, 2, 4])
            x1 = y*self.cell_width
            y1 = x*self.cell_height

            x2 = x1+self.cell_width-5
            y2 = y1+self.cell_height-5 

            self.print_num(self.board[x, y], x, y, x1, y1, x2, y2)

            self.print_board()

    def empty_indices(self):
        indices = []
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i, j] == 0:
                    indices.append((i, j))
        return indices

    def shift(self, arr, reverse=False):
        if reverse:
            arr = arr[::-1]
        for j in range(len(arr)-1, -1, -1):
            for i in range(j, len(arr)-1):
                if arr[i] == arr[i+1]:
                    arr[i] = 0 
                    arr[i+1] *= 2 
                    self.score += arr[i+1]
                if arr[i+1] == 0:
                    arr[i+1], arr[i] = arr[i], arr[i+1]
        if reverse:
            return arr[::-1]
        return arr

    def key_pressed(self, event):
        shift = 0 
        if event.keysym == 'Down':
            for i in range(self.N):
                self.board[:, i] = self.shift(self.board[:, i])
        elif event.keysym == 'Right':
            for i in range(self.N):
                self.board[i, :] = self.shift(self.board[i, :])
        elif event.keysym == 'Up':
            for i in range(self.N):
                self.board[:, i] = self.shift(self.board[:, i], True)
        elif event.keysym == 'Left':
            for i in range(self.N):
                self.board[i, :] = self.shift(self.board[i, :], True)
        self.print_board()
        self.add_new_tile()
        self.is_over()

    def get_adjacent_tiles(self, x, y):
        Indices = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
        New_Ind = []
        N = self.N
        for ind in Indices:
            if 0 <= ind[0] < N and 0 <= ind[1] < N:
                New_Ind.append(ind)
        return New_Ind

    def is_over(self):
        if not self.is_filled:
            return False

        for i in range(self.N):
            for j in range(self.N):
                curr_value = self.board[i, j]
                indices = self.get_adjacent_tiles(i, j)
                for ind in indices:
                    if self.board[ind[0], ind[1]] == curr_value or self.board[ind[0], ind[1]] == 0:
                        return False 

        game_over = []
        game_over += [['G', 'A', 'M', 'E'] + ['']*(self.N-4)]
        game_over += [['O', 'V', 'E', 'R'] + ['']*(self.N-4)]

        game_over += [['']*self.N]*(self.N-2)

        self.square = {}
        

        self.print_board()


        for row in range(self.N):
            for column in range(self.N):
                x1 = column*self.cell_width
                y1 = row*self.cell_height
                x2 = x1+self.cell_width-5
                y2 = y1+self.cell_height-5
                self.square[row,column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e0f2f8", tags="rect", outline="")
                self.canvas.create_text((x1 + x2)/2, (y1+y2)/2, font=("Arial", 36), fill="#494949", text=game_over[row][column])

        return True


def main():
    app = Game(4)
    app.bind_all('<Key>', app.key_pressed)
    app.wm_title("2048!")
    app.minsize(app.CANVAS_WIDTH, app.CANVAS_HIGHT)
    app.maxsize(app.CANVAS_WIDTH, app.CANVAS_HIGHT)

    app.mainloop()


if __name__ == "__main__":
    main()
