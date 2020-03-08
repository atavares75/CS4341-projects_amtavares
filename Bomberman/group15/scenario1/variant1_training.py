# This is necessary to find the main code
import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
sys.path.insert(1, '../group15')

from q_learner import qLearner
from q_entitiy import qEntity
from f_functions import *

QLearner = qLearner([f_to_closest_exit, f_to_closest_monster, f_to_closest_bomb, f_existing_bomb, f_is_exploded])

# Create the game
g = Game.fromfile('map.txt')