# This is necessary to find the main code
import sys
import csv
import datetime

sys.path.insert(0, '../../bomberman')
sys.path.insert(1, '..')

# Import necessary stuff
import random
from game import Game
from monsters.stupid_monster import StupidMonster
sys.path.insert(1, '../group15')

from q_learner import qLearner
from q_entity import qEntity
from f_functions import *
import os
import pickle

weights_file = get_weight_save_path(2)

csv_path = get_csv_save_path(2)

if os.path.exists(weights_file) and os.path.getsize(weights_file) > 0:
    f = open(weights_file, 'rb')
    weights = pickle.load(f)
else:
    weights = [1, -1, 1, -1, -1]
print(weights)
QLearner = qLearner(weights, [f_to_closest_exit, f_time_to_explosion, f_to_closest_monster, f_in_bomb_path, f_existing_bomb], learning_rate = 0.2)

start = datetime.datetime.now()
for i in range(0,1):
    print(f"Iteration #{i}")
    # Create the game
    random.seed(123)  # TODO Change this if you want different random choices
    g = Game.fromfile('map.txt')
    g.add_monster(StupidMonster("stupid",  # name
                                "S",  # avatar
                                3, 9  # position
                                ))

    # name, avatar, x, y, qLearner, iterNum, maxIterations, trainModel=False
    g.add_character(qEntity("me", "C", 0, 0, QLearner, 1000, True))

    # Run!
    g.go()

    # score = g.world.scores["me"]
    with open(csv_path, 'a')as scorescsv:
        writer = csv.writer(scorescsv)
        writer.writerow([g.world.scores["me"]])
    print(QLearner.weights)

end = datetime.datetime.now()
print(end-start)
pickle.dump(weights, open(weights_file, 'wb'))
