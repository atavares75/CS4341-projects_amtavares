import math
import random
import sys

sys.path.insert(0, '../bomberman')
from entity import CharacterEntity
from sensed_world import SensedWorld

class qEntity(CharacterEntity):

    def __init__(self, name, avatar, x, y, qLearner, iterNum, maxIterations, bombs = True, trainModel=False):
        CharacterEntity.__init__(name, avatar, x, y)

        #Includes other variables needed for q learning
        self.qLearner = qLearner
        self.trainModel = trainModel
        self.iterNum = iterNum
        self.maxIterations = maxIterations

        self.bombs = bombs
        self.exit = None

        self.previousWorld = None
        self.epsilon = math.sqrt(1 / 1 + iterNum)

    def do(self, wrld):
        self.previousWorld = wrld

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

                # Random chance of placing bomb
                if random.choice(bomb_choices) == 1:
                    self.place_bomb()

                # Make random move
                self.move(dx, dy)

            else:
                # Call Q-Learner
                move, _ = self.qLearner.best_move(wrld, self)
                dx, dy, bomb = move

                self.move(dx, dy)

                if bomb == 1:
                    self.place_bomb()

        else:
            # Call Q-Learner
            move, _ = self.qLearner.best_move(wrld, self)
            dx, dy, bomb = move

            self.move(dx, dy)

            if bomb == 1:
                self.place_bomb()

    # updates weights
    def done(self):
        pass


