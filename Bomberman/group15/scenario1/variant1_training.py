# This is necessary to find the main code
import sys

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
from game import Game
sys.path.insert(1, '../group15')

from q_learner import qLearner
from q_entity import qEntity
from f_functions import *
import os
import pickle

path = os.path.dirname(os.path.dirname(os.getcwd()))

weights_file = os.path.join(path, "Outputs/TrainingScores/variant1_weights.p")

weights = [0, 0, 0, 0, 0]

pickle.dump(weights, open(weights_file, 'wb'))

QLearner = qLearner([f_to_closest_exit, f_to_closest_monster, f_to_closest_bomb, f_existing_bomb, f_is_exploded])

for i in range(0,1):
    print(f"Iteration #{i}")

    # Create the game
    g = Game.fromfile('map.txt',)

    g.add_character(qEntity("me",  # name
                             "C",  # avatar
                              0, 0,  # position
                              QLearner, #qLearner
                              False,
                              i,
                              1000
                              ))

    # Run game
    g.go(1)

    score = g.world.scores["me"]
    print(g.world.scores)
    # if score > 0:
    #     QLearner.update_weights(g.world, g.world.characters["me"], 9999)
    # else:
    #     QLearner.update_weights(g.world, g.world.characters["me"], -9999)

    print(QLearner.pos, QLearner.move)
