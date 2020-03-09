# This is necessary to find the main code
import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game

# TODO This is your code!
sys.path.insert(1, '../group15')

from q_entity import qEntity
from q_learner import qLearner
from f_functions import *

QLearner = qLearner([56.073533967383526, -1.7236336915945127, -0.3652660210675589], [f_to_closest_exit, f_to_closest_bomb, f_time_to_explosion], learning_rate = 0.2)
# Create the game
g = Game.fromfile('map.txt')

# TODO Add your character

# Uncomment this if you want the test character
g.add_character(qEntity("me", "C", 0, 0, QLearner, 1000, False))

# Uncomment this if you want the interactive character
# g.add_character(InteractiveCharacter("me",  # name
#                                      "C",  # avatar
#                                      0, 0  # position
#                                      ))

# Run!

# Use this if you want to press ENTER to continue at each step
# g.go(0)

# Use this if you want to proceed automatically
g.go(1)
