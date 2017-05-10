from circuit import Circuit

class Node:
    def __init__(self, value,row,col):
        self.parent = None
        self.value = value
        self.row = row
        self.col = col
        self.gcost = 0
        self.fcost = 0

class AStarHandler:
    def __init__(self, heuristic):
        self.circuit = Circuit()
        self.matrix = [[0 for x in range(self.circuit.ROWS)]for y in range(self.circuit.COLS)]
        for row in range(self.circuit.ROWS):
            for col in range(self.circuit.COLS):
                self.matrix[row][col] = Node(self.circuit.pathM_[row][col],row,col)
        for key in self.circuit.wirePoints:
            path = astar(self.matrix[key[0]][key[1]],self.matrix[self.circuit.wirePoints[key][0]][self.circuit.wirePoints[key][1]],self.matrix, heuristic)
        for item in path:
            print(item.row, item.col)
def manhattan(curr, dest):
    #print(abs(curr.row - dest.row) + abs(curr.col - dest.col))
    return  abs(curr.row - dest.row) + abs(curr.col - dest.col)

def bfs(curr, dest):
    return 0
    
            
def neighbours(node,grid):
    neighboured = []
    if node.row-1>=0 and grid[node.row-1][node.col].value != 1:
        neighboured.append(grid[node.row-1][node.col])
    if node.row+1<len(grid) and grid[node.row+1][node.col].value != 1:
        neighboured.append(grid[node.row+1][node.col])
    if node.col-1>=0 and grid[node.row][node.col-1].value != 1:
        neighboured.append(grid[node.row][node.col-1])
    if node.col+1<len(grid) and grid[node.row][node.col+1].value != 1:
        neighboured.append(grid[node.row][node.col+1])
    return neighboured
        

def astar(start,dest,matrix, heuristic):
    openSet = set()
    closedSet = set()
    current = start
    current.gcost = 0
    current.fcost=heuristic(current,dest)
    openSet.add(current)
    counter = 0
    while(openSet):
        counter += 1
        current = min(openSet, key=lambda c: c.fcost)
        if current.row == dest.row and current.col == dest.col:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            print("Iterations: ", counter)
            return path[::-1]
        openSet.remove(current)
        closedSet.add(current)
        for node in neighbours(current,matrix):
            counter += 1
            if node in closedSet:
                continue
            if node in openSet:
                tentativegscore = current.gcost + 1
                if node.gcost > tentativegscore:
                    node.gcost = tentativegscore
                    node.parent = current
            else:
                node.gcost = current.gcost + 1
                node.fcost = node.gcost + heuristic(node,dest)
                node.parent = current
                openSet.add(node)
            
                                         

#import tkinter as tk
#root = tk.Tk()
#root.wm_title("Normal Pathfinding")
#buttonFrame = tk.Frame(root)
#buttonFrame.grid(row=2, column=0, columnspan=2)
#tk.Button(buttonFrame, text="AStar", command=lambda: AStarHandler(manhattan)).grid(row=0,column=1)
#tk.Button(buttonFrame, text="BFS", command=lambda: AStarHandler(bfs)).grid(row=0,column=2)
#buttonFrame.pack()            
#root.update()
#root.mainloop()
