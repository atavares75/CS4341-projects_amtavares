import math
import random
import sys

sys.path.insert(0, '../bomberman')
from entity import CharacterEntity
from sensed_world import SensedWorld
from f_functions import *


class qEntity(CharacterEntity):

    def __init__(self, name, avatar, x, y, qLearner, iterNum, maxIterations, trainModel):
        CharacterEntity.__init__(self, name, avatar, x, y)

        #Includes other variables needed for q learning
        self.qLearner = qLearner
        self.trainModel = trainModel
        self.iterNum = iterNum
        self.maxIterations = maxIterations

    def do(self, world):
        self.previousWorld = world
        self.iterNum += 1
        if self.iterNum == self.maxIterations:
            return
        randomChance = 1 / (self.iterNum + 1)
        bomb = 0
        dx = 0
        dy = 0
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
            move, _ = self.qLearner.best_move(world, self)
            dx, dy, bomb = move
            if bomb == 1:
                self.place_bomb()
            self.move(dx, dy)

        if self.trainModel:
            new_world = SensedWorld.from_world(world)
            if bomb == 1:
                new_world.me(self).place_bomb()
            new_world.me(self).move(dx, dy)
            new_world, _ = new_world.next()
            self.qLearner.updateWeights(self.previousWorld, new_world, self, 0)


    # updates weights
    def done(self, wrld):
        print("Updating")
        if self.trainModel:
            reward = 0
            for event in wrld.events:
                if event.tpe == Event.BOMB_HIT_CHARACTER:
                    reward = -50
                    break
                if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                    reward = -50
                    break
                if event.tpe == Event.CHARACTER_FOUND_EXIT:
                    reward = 100
                    break
            if reward == 0:
                reward = ((f_to_closest_exit(wrld, self))*5 - (f_to_closest_monster(wrld, self)**.2))

            self.qLearner.updateWeights(self.previousWorld, wrld, self, reward)




