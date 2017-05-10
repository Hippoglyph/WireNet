import ast
import copy
import tkinter as tk

class Wire:
	def __init__(self, name, startC, startR, goalC, goalR, color):
		self.name = name
		self.startC = startC
		self.startR = startR
		self.c = startC
		self.r = startR
		self.goalC = goalC
		self.goalR = goalR
		self.amountTurns = 0
		self.length = 1
		self.directionR = 0
		self.directionC = 0
		self.connected = False
		self.color = color
		self.path = []
		self.path.append((self.r,self.c))


class Circuit:
	def __init__(self):
		f = open("generatedInput", "r")
		self.ROWS = int(f.readline())
		self.COLS = int(f.readline())
		self.pathM_ = ast.literal_eval(f.readline())
		self.wireCount = int(f.readline())
		self.wirePoints = ast.literal_eval(f.readline())

		if(len(self.pathM_) != self.ROWS or len(self.pathM_[0]) != self.COLS or len(self.wirePoints.keys()) != self.wireCount):
			print ("Error: incorrect input file")
		f.close()
		self.wireColors = {}
		for key in self.wirePoints:
			self.wireColors[key] = self.pathM_[key[0]][key[1]]
			self.pathM_[key[0]][key[1]] = 1
			self.pathM_[self.wirePoints[key][0]][self.wirePoints[key][1]] = 0 

		self.wires = {}

	def start(self):
		self.wires.clear()
		self.pathM = copy.deepcopy(self.pathM_)
		wireIndex = 0
		for key in self.wirePoints.keys():
			name = "Wire"+str(wireIndex)
			self.wires[name] = Wire(name, key[1], key[0], self.wirePoints[key][1], self.wirePoints[key][0], self.wireColors[key])
			wireIndex+=1

	def restart(self):
		self.start()

	def getWires(self):
		return self.wires.keys()

	def getPathMatrixSize(self):
		return self.ROWS*self.COLS

	def getRows(self):
		return self.ROWS

	def getCols(self):
		return self.COLS

	def getWirePosition(self, wireName):
		if wireName not in self.wires:
			print ("Error: " + wireName + " does not exists")
		return (self.wires[wireName].r,self.wires[wireName].c)

	def getWireGoal(self, wireName):
		if wireName not in self.wires:
			print ("Error: " + wireName + " does not exists")
		return (self.wires[wireName].goalR, self.wires[wireName].goalC)

	def getPathMatrix(self):
		return self.pathM

	def move(self, wireName, rowOff, colOff):
		if wireName not in self.wires:
			print ("Error: " + wireName + " does not exists")
			return False
		wire = self.wires[wireName]
		if(wire.connected):
			return False
		if (wire.c+colOff < 0) or (wire.c+colOff >= self.COLS) or (wire.r+rowOff < 0) or (wire.r+rowOff >= self.ROWS):
			return False
		if self.pathM[wire.r+rowOff][wire.c+colOff] != 0:
			return False
		self.pathM[wire.r+rowOff][wire.c+colOff] = 1
		if((wire.directionC != colOff) or (wire.directionR != rowOff)):
			wire.amountTurns += 1
			wire.directionC = colOff
			wire.directionR = rowOff
		wire.length += 1
		wire.c += colOff
		wire.r += rowOff
		wire.path.append((wire.r,wire.c))
		if(wire.c == wire.goalC and wire.r == wire.goalR):
			wire.connected = True
		return True

	def moveNorth(self, wireName):
		return self.move(wireName, -1, 0)

	def moveSouth(self, wireName):
		return self.move(wireName, 1, 0)

	def moveWest(self, wireName):
		return self.move(wireName, 0, -1)

	def moveEast(self, wireName):
		return self.move(wireName, 0, 1)

	def isDone(self):
		for wire in self.wires:
			if not self.wires[wire].connected:
				return False
		return True

	def getTotalTurns(self):
		turns = 0
		for wire in self.wires:
			turns += self.wires[wire].amountTurns
		return turns

	def getWireLength(self):
		length = 0
		for wire in self.wires:
			length += self.wires[wire].length
		return length

	def getCompletedWires(self):
		amount = 0
		for wire in self.wires:
			if self.wires[wire].connected:
				amount += 1
		return amount

	def printPathMatrix(self):
		print("--------")
		for row in self.pathM:
			print (row)
		print("--------")

	def getFitness(self):
		return self.getCompletedWires()*50 - self.getWireLength()*2 - self.getTotalTurns()

	def drawResult(self):
		c = None
		root = tk.Tk()
		root.wm_title("WireNet - Result")
		buttonFrame = tk.Frame(root)
		buttonFrame.grid(row=2, column=0, columnspan=2)
		tk.Button(buttonFrame, text="Draw Base", command=lambda: self.drawBase(c, root)).grid(row=0, column=0)
		tk.Button(buttonFrame, text="Draw Wired", command=lambda: self.drawWired(c, root)).grid(row=0, column=1)
		buttonFrame.pack()
		c = tk.Canvas(root, width=500, height=500,   background='white')
		c.pack()
		root.update()
		self.drawWired(c, root)
		root.mainloop()

	def drawBase(self, canvas, root):
		canvas.delete("all")
		col_width = canvas.winfo_width()/self.COLS
		row_height = canvas.winfo_height()/self.ROWS
		for row in range(self.ROWS):
			for col in range(self.COLS):
				color = self.pathM_[row][col]
				if color == 0:
					color = "white"
				elif color == 1:
					color = "black"
				canvas.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=color, outline="black")
		for wireName in self.wires:
			wire = self.wires[wireName]
			color = wire.color
			canvas.create_rectangle(wire.startC*col_width, wire.startR*row_height, (wire.startC+1)*col_width, (wire.startR+1)*row_height, fill=color, outline="black")
			canvas.create_rectangle(wire.goalC*col_width, wire.goalR*row_height, (wire.goalC+1)*col_width, (wire.goalR+1)*row_height, fill=color, outline="black")
		root.update()

	def drawWired(self, canvas, root):
		canvas.delete("all")
		col_width = canvas.winfo_width()/self.COLS
		row_height = canvas.winfo_height()/self.ROWS
		for row in range(self.ROWS):
			for col in range(self.COLS):
				color = self.pathM_[row][col]
				if color == 0:
					color = "white"
				elif color == 1:
					color = "black"
				canvas.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=color, outline="black")
		for wireName in self.wires:
			wire = self.wires[wireName]
			color = wire.color
			for row, col in wire.path:
				canvas.create_rectangle(col*col_width, row*row_height, (col+1)*col_width, (row+1)*row_height, fill=color, outline="black")
			canvas.create_rectangle((wire.startC+0.4)*col_width, (wire.startR+0.4)*row_height, (wire.startC+0.6)*col_width, (wire.startR+0.6)*row_height, fill=color, outline="black")
			canvas.create_rectangle((wire.goalC+0.4)*col_width, (wire.goalR+0.4)*row_height, (wire.goalC+0.6)*col_width, (wire.goalR+0.6)*row_height, fill=color, outline="black")
		root.update()