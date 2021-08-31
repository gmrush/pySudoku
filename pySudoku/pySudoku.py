# George Rush | August 2021
# Sudoku game + solver

from tkinter import *
import sys

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("pySudoku")
        self.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))
        self.resizable(False, False)

SQUARE_SIZE = 80
WIN_HEIGHT = 720
WIN_WIDTH = 720
GRID = [0] * 81
ROOT = Root()
INDEX = 0
C = Canvas(ROOT, width=900, height=900)
BOXES = [[0, 1, 2, 9, 10, 11, 18, 19, 20],
         [3, 4, 5, 12, 13, 14, 21, 22, 23],
         [6, 7, 8, 15, 16, 17, 24, 25, 26],
         [27, 28, 29, 36, 37, 38, 45, 46, 47],
         [30, 31, 32, 39, 40, 41, 48, 49, 50],
         [33, 34, 35, 42, 43, 44, 51, 52, 53],
         [54, 55, 56, 63, 64, 65, 72, 73, 74],
         [57, 58, 59, 66, 67, 68, 75, 76, 77],
         [60, 61, 62, 69, 70, 71, 78, 79, 80]]

def clickEvent(event):
    global INDEX
    INDEX = int(event.x // SQUARE_SIZE) + int((event.y // SQUARE_SIZE) * 9) #index from click

def pressEvent(event):
    if str(event.char) in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        GRID[INDEX] = int(event.char)
    elif str(event.char) == " ":
        solve()
    drawCanvas()

def drawCanvas():
    C.delete('all')
    x, y = 0, 0
    for i in range(len(GRID)):
        if i % 9 == 0 and i != 0:
            y += SQUARE_SIZE
            x = 0
        C.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill="white", outline="black")
        if GRID[i] != 0:
            C.create_text((x + (SQUARE_SIZE / 2), y + (SQUARE_SIZE / 2)), text=str(GRID[i]), font="Courier 32")
        else:
            C.create_text((x + (SQUARE_SIZE / 2), y + (SQUARE_SIZE / 2)), text=" ", font="Courier 32")
        x += SQUARE_SIZE

def solve():
    global GRID
    print("Solving...")
    recur(GRID)
    drawCanvas()
    print("Solved!")

def recur(array):
    global GRID
    for i in range(len(GRID)):
        if array[i] == 0:
            for n in range(1, 10):
                if checkSpace(i, array, n):
                    array[i] = n
                    if recur(array):
                        return True
                    else: array[i] = 0
            return False
    GRID = array
    return True

def checkSpace(pos, array, n):
    if checkColumn(pos, array, n) and checkRow(pos, array, n) and checkBox(pos, array, n): return True
    else: return False

def checkColumn(pos, array, n): #check column doesnt already contain number
    num = n
    traverse = pos
    while traverse - 9 >= 0: #move up
        traverse -= 9
        if array[traverse] == num: return False
    traverse = pos
    while traverse + 9 < 81: #move down
        traverse += 9
        if array[traverse] == num: return False
    return True

def checkRow(pos, array, n): #check row doesnt already contain number
    num = n
    traverse = pos
    rowStart = (pos // 9) * 9
    rowEnd = rowStart + 9
    while traverse - 1 >= rowStart: #move left
        traverse -= 1
        if array[traverse] == num: return False
    traverse = pos
    while traverse + 1 < rowEnd: #move right
        traverse += 1
        if array[traverse] == num: return False
    return True

def checkBox(pos, array, n): #most definitley can make this faster using some form of hashing
    num = n
    boxNum = -1
    for i in range(9): #9 boxes
        for n in range(9): #9 numbers in each box
            if pos == BOXES[i][n]: #find box containing position
                boxNum = i
                break
    for i in range(9):
        if array[BOXES[boxNum][i]] == num:
            if BOXES[boxNum][i] != pos:
                return False
    return True

def sudoku():
    drawCanvas()
    C.bind("<Button-1>", clickEvent)
    C.pack()
    ROOT.bind("<KeyPress>", pressEvent)
    ROOT.mainloop()

if __name__ == "__main__":
    sudoku()
