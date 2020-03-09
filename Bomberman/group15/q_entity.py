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
        self.iterNum += 1
        if self.iterNum == self.maxIterations:
            return
        randomChance = 1 / (self.iterNum + 1) ** .5
        if self.trainModel and random.random() < randomChance:
            moves = [-1,0,1]
            dx = random.choice(moves)
            dy = random.choice(moves)
            bombs = random.choice([0,1])
            if bombs == 1:
                self.place_bomb()
            self.move(dx,dy)

        else:
            # Call Q-Learner
            q, move = self.qLearner.best_move(world, self)
            dx, dy, bomb = move
            if bomb == 1:
                self.place_bomb()
            self.move(dx, dy)
        self.previousWorld = world



    # updates weights
    def done(self, wrld):
        print("Done")
        if self.trainModel:
            reward = 0
            for event in wrld.events:
                if wrld.me(self) == None and event.tpe == Event.BOMB_HIT_CHARACTER:
                    q = -50
                if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                    q = -50
                if event.tpe == Event.CHARACTER_FOUND_EXIT:
                    reward = 100
                    break
            if reward == 0:
                reward = ((f_to_closest_exit(wrld, self)**.2)*5 - (f_to_closest_monster(wrld, self)**.2))

            self.qLearner.updateWeights(self.previousWorld, wrld, self, reward)



