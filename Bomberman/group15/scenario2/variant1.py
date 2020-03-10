# This is necessary to find the main code
import sys
sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group15')
from testcharacter import TestCharacter

from q_entity import qEntity
from q_learner import qLearner
from f_functions import *

QLearner = qLearner([33.52188643440364, 56.35697559976078, -6.919527059531207, -1.8667396730207093], [f_diagonal_distance, f_distance_closest_monster, f_in_bomb_path, f_existing_bomb], learning_rate = 0.2)
# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character
g.add_character(qEntity("me", "C", 0, 0, QLearner, 1000, False))

# Run!
g.go(1)
