import os
import neat
from circuit import Circuit
import fileinput
import sys
import re

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

def editConfig(config_file):
    c = Circuit()
    c.start()
    numInput = c.getPathMatrixSize()
    numInput += len(c.getWires())*4
    numOutput = len(c.getWires())*4
    inputSearch = "^num_inputs\s+=\s+(\d)+(\n)?$"
    inputReplace = "num_inputs              = " + str(numInput) + "\n"
    outputSearch = "^num_outputs\s+=\s+(\d)+(\n)?$"
    outputReplace = "num_outputs             = " + str(numOutput) + "\n"
    for line in fileinput.input(config_file, inplace = 1): 
        line = re.sub(inputSearch, inputReplace, line)
        line = re.sub(outputSearch, outputReplace, line)
        sys.stdout.write(line)
    print ("Config file edited")

if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    editConfig(config_path)
    #run(config_path)