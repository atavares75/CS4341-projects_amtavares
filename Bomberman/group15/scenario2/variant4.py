# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.selfpreserving_monster import SelfPreservingMonster

# TODO This is your code!
sys.path.insert(1, '../group15')
from testcharacter import TestCharacter
from q_entity import qEntity
from q_learner import qLearner
from f_functions import *

QLearner = qLearner([16.333041369627114, 13.902204928021265, -0.8342853948255601, 14.9022198433055], [f_diagonal_distance, f_distance_closest_monster, f_in_bomb_path, f_existing_bomb], learning_rate = 0.2)


# Create the game
random.seed(123) # TODO Change this if you want different random choices
g = Game.fromfile('map.txt')
g.add_monster(SelfPreservingMonster("aggressive", # name
                                    "A",          # avatar
                                    3, 13,        # position
                                    2             # detection range
))

# TODO Add your character
g.add_character(qEntity("me", "C", 0, 0, QLearner, 1000, False))

# Run!
g.go(1)
