# This is necessary to find the main code
import sys
import csv
import datetime

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

weights_file = get_weight_save_path(1)

csv_path = get_csv_save_path(1)

if os.path.exists(weights_file) and os.path.getsize(weights_file) > 0:
    f = open(weights_file, 'rb')
    weights = pickle.load(f)
else:
    weights = [1, -1, -1]
print(weights)
QLearner = qLearner(weights, [f_to_closest_exit, f_to_closest_bomb, f_time_to_explosion], learning_rate = 0.2)

start = datetime.datetime.now()
for i in range(0,1):
    print(f"Iteration #{i}")
    # Create the game
    g = Game.fromfile('map.txt',)

    # name, avatar, x, y, qLearner, iterNum, maxIterations, trainModel=False
    g.add_character(qEntity("me", "C", 0, 0, QLearner, 1000, True))

    # Run game
    g.go(1)
    # score = g.world.scores["me"]
    with open(csv_path, 'a')as scorescsv:
        writer = csv.writer(scorescsv)
        writer.writerow([g.world.scores["me"]])
    print(QLearner.weights)

end = datetime.datetime.now()
print(end-start)
pickle.dump(weights, open(weights_file, 'wb'))
