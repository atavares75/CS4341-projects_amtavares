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


if os.path.exists("../../Outputs/TrainingScores/variant1_weights.p") and os.path.getsize("../../Outputs/TrainingScores/variant1_weights.p") > 0:
    print("Found weights")
    weights_file = "../../Outputs/TrainingScores/variant1_weights.p"
    wf = open(weights_file, 'rb')
    f = pickle.Unpickler(wf)
    weights = f.load()
else:
    weights_file = os.path.join(path, "Outputs/TrainingScores/variant1_weights.p")
    weights = [0,0,0,0,0]
    wf = open(weights_file, 'wb')
    pickle.dump(weights, wf)

QLearner = qLearner(weights, [f_to_closest_exit, f_to_closest_monster, f_to_closest_bomb, f_existing_bomb, f_time_to_explosion], learning_rate = 0.4)
print(QLearner.weights)
for i in range(0,1):
    print(f"Iteration #{i}")

    # Create the game
    g = Game.fromfile('map.txt',)

    # name, avatar, x, y, qLearner, iterNum, maxIterations, trainModel=False
    g.add_character(qEntity("me", "C", 0, 0, QLearner, i, 1000, True))

    # Run game
    g.go(1)

    score = g.world.scores["me"]
    print(g.world.scores)
    # if score > 0:
    #     QLearner.update_weights(g.world, g.world.characters["me"], 9999)
    # else:
    #     QLearner.update_weights(g.world, g.world.characters["me"], -9999)

    print(QLearner.weights)
    pickle.dump(weights, open(weights_file, 'wb'))