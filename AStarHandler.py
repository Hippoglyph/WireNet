from circuit import Circuit
import itertools
import copy

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
        self.circuit.start()
        self.bestPerformer = copy.deepcopy(self.circuit)
        self.matrix = [[0 for x in range(self.circuit.ROWS)]for y in range(self.circuit.COLS)]
        self.updateMatrix()
        for wiresPermut in itertools.permutations(self.circuit.getWires(), len(self.circuit.getWires())):
            #print(wiresPermut)
            for wireKey in wiresPermut:
                #print(wireKey)
                wire = self.circuit.wires[wireKey]
                start = self.matrix[wire.startR][wire.startC]
                dest = self.matrix[wire.goalR][wire.goalC]
                path = astar(start,dest,self.matrix, heuristic)
                if len(path)<1:
                    continue
                current = path[0]
                for item in path:
                    move = item.row-current.row,item.col-current.col
                    #print(move)
                    #print(item.row, item.col)
                    self.circuit.move(wireKey, move[0],move[1])
                    current = item
                self.updateMatrix()
                #self.circuit.printPathMatrix()
            #print("circuit fitness: ",self.circuit.getFitness()," Best performer fitness " ,self.bestPerformer.getFitness())
            
            if(int(self.circuit.getFitness())>int(self.bestPerformer.getFitness())):
                #print("Updated best")
                self.bestPerformer = copy.deepcopy(self.circuit)
            self.circuit.restart()
            self.updateMatrix()
        #print("Best performer has fitness: ", self.bestPerformer.getFitness())
        print("Turns: " + str(self.bestPerformer.getTotalTurns()))
        print("WireLength: "+str(self.bestPerformer.getWireLength()))
        print("Completed Wires: "+str(self.bestPerformer.getCompletedWires()))
        print("Fitness: "+str(self.bestPerformer.getFitness()))
        self.bestPerformer.drawResult()
        

    def updateMatrix(self):
        for row in range(self.circuit.ROWS):
            for col in range(self.circuit.COLS):
                self.matrix[row][col] = Node(self.circuit.pathM[row][col],row,col)
                #print(self.matrix[row][col].value)
        for wireKey in self.circuit.getWires():
            wire = self.circuit.wires[wireKey]
            #print(wire.goalR, wire.goalC)
            self.matrix[wire.goalR][wire.goalC].value=2
        
            
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
    #print(dest.row, dest.col)
    #print(start)
    openSet = []
    closedSet = []
    current = start
    current.gcost = 0
    current.fcost=heuristic(current,dest)
    openSet.append(current)
    counter = 0
    while(openSet):
        counter += 1
        current = min(openSet, key=lambda c: c.fcost)
        for neg in neighbours(current, matrix):
            if(dest.row == neg.row and dest.col == neg.col):
                #print("Reached!!!")
                path = []
                dest.parent = current
                current = dest
                while current.parent:
                    #print(current.row, current.col)
                    path.append(current)
                    current = current.parent
                path.append(current)
                #print("Iterations: ", counter)
                return path[::-1]
        openSet.remove(current)
        closedSet.append(current)
        for node in neighbours(current,matrix):
            if node.value == 2:
                continue
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
                openSet.append(node)
    return []   
                                         


#A = AStarHandler(manhattan)

