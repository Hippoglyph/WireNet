import os
import neat
from circuit import Circuit
import fileinput
import sys
import re
import visualize

class neatHandler:
    def __init__(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'config')
        self.circuit = Circuit()
        self.circuit.start()
        self.wireNames = self.circuit.getWires()
        self.numInputs = self.circuit.getPathMatrixSize() + len(self.wireNames)*4
        self.numOutputs = len(self.wireNames)*4
        self.editConfig(config_path)
        self.bestFitness = -999999
        self.stats = None
        self.run(config_path)

    def editConfig(self, config_path):
        inputSearch = "^num_inputs\s+=\s+(\d)+(\n)?$"
        inputReplace = "num_inputs              = " + str(self.numInputs) + "\n"
        outputSearch = "^num_outputs\s+=\s+(\d)+(\n)?$"
        outputReplace = "num_outputs             = " + str(self.numOutputs) + "\n"
        for line in fileinput.input(config_path, inplace = 1): 
            line = re.sub(inputSearch, inputReplace, line)
            line = re.sub(outputSearch, outputReplace, line)
            sys.stdout.write(line)
        print ("Config file edited")

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            genome.fitness = self.evalNet(net)
            if self.bestFitness < genome.fitness:
                self.bestFitness = genome.fitness
                print("New Best Fitness: "+str(self.circuit.getFitness()))
                self.circuit.drawResult()
                visualize.plot_stats(self.stats, ylog=False, view=True)
            
    def evalNet(self, net):
        self.circuit.restart()
        while not(self.circuit.isDone()):
            output = net.activate(self.getInputsForCircuit())
            if not self.makeMove(output):
                break
        return self.circuit.getFitness()

    def makeMove(self, output):
        moves = self.getMoveList(output)
        for move in moves:
            if move[0](move[2]):
                return True
        return False

    def getMoveList(self, output):
        i = 0
        moves = []
        for wire in self.wireNames:
            moves.append((self.circuit.moveNorth, output[i], wire))
            i+=1
            moves.append((self.circuit.moveEast, output[i], wire))
            i+=1
            moves.append((self.circuit.moveSouth, output[i], wire))
            i+=1
            moves.append((self.circuit.moveWest, output[i], wire))
            i+=1
        moves.sort(key=lambda tup: tup[1])
        return moves

    def getInputsForCircuit(self):
        inputs = []
        for row in self.circuit.getPathMatrix():
            for i in row:
                inputs.append(i)
        for wire in self.wireNames:
            srow,scol = self.circuit.getWirePosition(wire)
            inputs.append(srow / self.circuit.getRows())
            inputs.append(scol / self.circuit.getCols())
            grow,gcol = self.circuit.getWireGoal(wire)
            inputs.append(grow / self.circuit.getRows())
            inputs.append(gcol / self.circuit.getCols())
        return inputs


    def run(self, config_file):
        # Load configuration.
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_file)

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        p.add_reporter(self.stats)

        # Run for up to 300 generations.
        winner = p.run(self.eval_genomes, 1000)
        self.evalNet(neat.nn.FeedForwardNetwork.create(winner, config))
        #os.system("/usr/bin/canberra-gtk-play --id='bell'")

        #visualize.draw_net(config, winner, True)
        visualize.plot_stats(self.stats, ylog=False, view=True)
        #visualize.plot_species(stats, view=True)

        print("Turns: " + str(self.circuit.getTotalTurns()))
        print("WireLength: "+str(self.circuit.getWireLength()))
        print("Completed Wires: "+str(self.circuit.getCompletedWires()))
        print("Fitness: "+str(self.circuit.getFitness()))
        self.circuit.drawResult()

        # Display the winning genome.
        #print('\nBest genome:\n{!s}'.format(winner))

        
        #print('\nOutput:')
        #winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

n = neatHandler()
