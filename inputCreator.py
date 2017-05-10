import tkinter as tk
import random
import sys
from AStarHandler import AStarHandler
from AStarHandler import manhattan
from AStarHandler import bfs


ROWS = sys.argv[1] if len(sys.argv) > 1 else 10
COLS = sys.argv[2] if len(sys.argv) > 2 else 10
placeCounter = 0
tiles = [[0 for _ in range(COLS)] for _ in range(ROWS)]
boardinfo = [[None for _ in range(COLS)] for _ in range(ROWS)]
wirePoints = {}
def randomColor():
    r = random.randint(0,255)
    b = random.randint(0,255)
    g = random.randint(0,255)
    return htmlcolor(r,b,g)

def updateCounter(row,col):
    global placeCounter, color, dest, start;
    placeCounter += 1
    #print(placeCounter)
    if(placeCounter == 2):
        placeCounter = 0
        color = randomColor()

def htmlcolor(r, g, b):
    def _chkarg(a):
        if isinstance(a, int): # clamp to range 0--255
            if a < 0:
                a = 0
            elif a > 255:
                a = 255
        elif isinstance(a, float): # clamp to range 0.0--1.0 and convert to integer 0--255
            if a < 0.0:
                a = 0
            elif a > 1.0:
                a = 255
            else:
                a = int(round(a*255))
        else:
            raise ValueError('Arguments must be integers or floats.')
        return a
    r = _chkarg(r)
    g = _chkarg(g)
    b = _chkarg(b)
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def wall(event):
    # Get rectangle diameters
    col_width = c.winfo_width()/COLS
    row_height = c.winfo_height()/ROWS

    col = int(event.x//col_width)
    row = int(event.y//row_height)
    #print("Pressed tile: ", tiles[row][col])

    if tiles[row][col] == 0:
        #print("Created rectangle from xPos: ", col*col_width, " yPos: ", row*row_height, " with width: ", col_width, " and height: ",row_height)
        c.itemconfig(boardinfo[row][col], fill="black")
        tiles[row][col] = 1
    # If the tile is already clicked, change colour but dont remove outline
    else:
        c.itemconfig(boardinfo[row][col],fill="white")
        tiles[row][col] = 0

def start(event):
    # Get rectangle diameters
    col_width = c.winfo_width()/COLS
    row_height = c.winfo_height()/ROWS

    col = int(event.x//col_width)
    row = int(event.y//row_height)
    #print("Pressed tile: ", tiles[row][col])

    if tiles[row][col] == 0:
        #print("Created rectangle from xPos: ", col*col_width, " yPos: ", row*row_height, " with width: ", col_width, " and height: ",row_height)
        c.itemconfig(boardinfo[row][col], fill=color)
        tiles[row][col] = color
        updateCounter(row,col)
        
    # If the tile is already clicked, change colour but dont remove outline
    else:
        c.itemconfig(boardinfo[row][col],fill="white")
        tiles[row][col] = 0


def reset():
    global placeCounter, tiles, boardinfo, wirePoints
    wirePoints = {}
    c.delete("all")
    tiles = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    boardinfo = [[None for _ in range(COLS)] for _ in range(ROWS)]
    placeCounter = 0
    col_width = c.winfo_width()/COLS
    row_height = c.winfo_height()/ROWS
    for y in range(ROWS):
            col = int(y)
            for x in range(COLS):
                    row = int(x)
                    tiles[x][y] = 0
                    boardinfo[x][y] = c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="white", outline="black")


def increaseSize():
    global ROWS, COLS
    ROWS+=1
    COLS+=1
    reset()

def decreaseSize():
    global ROWS,COLS
    ROWS-=1
    COLS-=1
    reset()

def findMate(row, col, color):
    for x in range(ROWS):
        for y in range(COLS):
            if(tiles[x][y] == color and (x,y) != (row,col)):
                return (x,y)

def createOutputArray():
    global wirePoints
    wirePoints = {}
    for x in range(ROWS):
        for y in range(COLS):
            if(tiles[x][y] != 1 and tiles[x][y] != 0 and (x,y) not in wirePoints.values()):
                found = findMate(x,y,tiles[x][y])
                if found is not None:
                    wirePoints[(x,y)] = found
                #print("row: ", x, " column: ", y, " color: ", tiles[x][y])
    #print(wirePoints)
    f = open('generatedInput','w')
    f.write(str(ROWS))
    f.write("\n")
    f.write(str(COLS))
    f.write("\n")
    f.write(str(tiles))
    f.write("\n")
    f.write(str(len(wirePoints)))
    f.write("\n")
    f.write(str(wirePoints))
    f.close()



color = randomColor()
# Create the window, a canvas and the mouse click event binding
root = tk.Tk()
root.wm_title("Cool AF")
buttonFrame = tk.Frame(root)
buttonFrame.grid(row=2, column=0, columnspan=5)
tk.Button(buttonFrame, text="Reset", command=reset).grid(row=0, column=0)
tk.Button(buttonFrame, text="Increase grid size", command=increaseSize).grid(row=0, column=1)
tk.Button(buttonFrame, text="Decrease grid size", command=decreaseSize).grid(row=0, column=2)
tk.Button(buttonFrame, text="Create output", command=createOutputArray).grid(row=0, column=3)
tk.Button(buttonFrame, text="AStar", command=lambda: AStarHandler(manhattan)).grid(row=0,column=4)
tk.Button(buttonFrame, text="BFS", command=lambda: AStarHandler(bfs)).grid(row=0,column=5)
buttonFrame.pack()


c = tk.Canvas(root, width=500, height=500,   background='white')
c.pack()
root.update()
col_width = c.winfo_width()/COLS
row_height = c.winfo_height()/ROWS
for y in range(ROWS):
        col = int(y)
        for x in range(COLS):
                row = int(x)
                tiles[x][y] = 0
                boardinfo[x][y] = c.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill="white", outline="black")

c.bind("<1>", wall)
c.bind("<Shift-1>", start)



root.mainloop()
