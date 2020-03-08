import math
import random
import sys


sys.path.insert(0, '../bomberman')
from entity import CharacterEntity
from sensed_world import SensedWorld
from f_functions import *
from events import Event

class qEntity(CharacterEntity):

    def __init__(self, name, avatar, x, y, qLearner, iterNum, maxIterations, trainModel=False):
        CharacterEntity.__init__(self, name, avatar, x, y)

        #Includes other variables needed for q learning
        self.qLearner = qLearner
        self.trainModel = trainModel
        self.iterNum = iterNum
        self.maxIterations = maxIterations
        self.previousWorld = None


    def do(self, world):
        self.previousWorld = world
        randomChance = 1 / math.sqrt(self.iterNum + 1)
        if self.trainModel and random.random() < randomChance:
            moves = [-1,0,1]

            dx = random.choice(moves)
            dy = random.choice(moves)
            bombs = random.choice(moves[1:])

            if bombs == 1:
                self.place_bomb()
            self.move(dx,dy)

        else:
            # Call Q-Learner
            q, move, r = self.qLearner.best_move(world, self)
            dx, dy, bomb = move

            self.move(dx, dy)
            if bomb == 1:
                self.place_bomb()



    # updates weights
    def done(self, wrld):
        print("Done")
        if self.trainModel:
            if wrld.me(self) == None:
                for event in wrld.events:
                    if event.tpe == Event.BOMB_HIT_CHARACTER or event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                        reward = -9999
                    if event.tpe == Event.CHARACTER_FOUND_EXIT:
                        reward = 9999
            else:
                reward = ((f_to_closest_exit(wrld, self))*5 - (f_to_closest_monster(wrld, self)**.2))

            self.qLearner.updateWeights(self.previousWorld, wrld, self, reward)



