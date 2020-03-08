import math
import random
import sys

sys.path.insert(0, '../bomberman')
from entity import CharacterEntity
from sensed_world import SensedWorld
from f_functions import *

class qEntity(CharacterEntity):

<<<<<<< HEAD
    def __init__(self, name, avatar, x, y, qLearner, iterNum, maxIterations, trainModel=False):
        CharacterEntity.__init__(name, avatar, x, y)
=======
    def __init__(self, name, avatar, x, y, qLearner, trainModel, iterNum, maxIterations, bombs=True):
        CharacterEntity.__init__(self, name, avatar, x, y)

>>>>>>> 2d60a0b56d43a4db843fcba75390d43b628ae0e1
        #Includes other variables needed for q learning
        self.qLearner = qLearner
        self.trainModel = trainModel
        self.iterNum = iterNum
        self.maxIterations = maxIterations
<<<<<<< HEAD
        self.oldWorld = None
=======

        self.bombs = bombs
        self.exit = None

        self.previousWorld = None
        self.epsilon = math.sqrt(1 / 1 + iterNum)

    def do(self, wrld):
        self.previousWorld = wrld
        self.qLearner.pos = (self.x, self.y)

        if self.trainModel:
            # e-greedy Exploration check
            if random.random() < self.epsilon:
                # Pick a random move
                move_choices = [-1,0,1]

                if self.bombs:
                    bomb_choices = [0,1]
                else:
                    bomb_choices = [0]

                dx = random.choice(move_choices)
                dy = random.choice(move_choices)
                rbomb = random.choice(bomb_choices)
>>>>>>> 2d60a0b56d43a4db843fcba75390d43b628ae0e1

                self.qLearner.move = (dx, dy, rbomb)
                # Random chance of placing bomb
                if rbomb == 1:
                    self.place_bomb()

<<<<<<< HEAD
    def do(self, world):
        self.oldWorld = world
        randomChance = 1 / math.sqrt(self.iterNum + 1)
        if self.trainModel and random.random() < randomChance:
            moves = [-1,0,1]

            dx = random.choice(moves)
            dy = random.choice(moves)
            bombs = random.choice(moves[1:])
            if bombs == 1:
                self.placeBomb()
            self.move(dx,dy)
=======
                # Make random move
                self.move(dx, dy)

            else:
                # Call Q-Learner
                move, _ = self.qLearner.best_move(wrld, self)
                self.qLearner.move = move

                dx, dy, bomb = move

                self.move(dx, dy)

                if bomb == 1:
                    self.place_bomb()

>>>>>>> 2d60a0b56d43a4db843fcba75390d43b628ae0e1
        else:
            # Call Q-Learner
            move, _ = self.qLearner.best_move(wrld, self)
            dx, dy, bomb = move

            self.move(dx, dy)

            if bomb == 1:
                self.place_bomb()

    # updates weights
    def update_weights(self, wrld, win, lose):
        if self.trainModel:
            if win:
                reward = 9999
            elif lose:
                reward = -9999
            else:
                reward = ((f_to_exit(wrld, self)**.2)*5 - (f_to_monster(wrld, self)**.2))

            self.qLearner.update_weights(wrld, self, reward)



