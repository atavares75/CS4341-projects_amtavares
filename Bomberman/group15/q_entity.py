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
        self.previousWorld = None


    def do(self, world):
        self.previousWorld = world
        randomChance = 1 / math.sqrt(self.iterNum + 1)
        if self.trainModel and random.random() < self.randomChance:
            moves = [-1,0,1]

            dx = random.choice(moves)
            dy = random.choice(moves)

            if self.bombs:
                bombs = random.choice(moves[1:2])
                if bombs == 1:
                    self.placeBomb()
            self.move(dx,dy)
        else:
            # call Q-Learner
            pass

    #updates weights
    def done(self):
        pass


