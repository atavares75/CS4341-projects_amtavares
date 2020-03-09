# This is necessary to find the main code
import math
import sys
sys.path.insert(0, '../bomberman')

from f_functions import *
from events import Event
from sensed_world import SensedWorld

import os
import pickle

# Training Values
GAMMA = .9
ALPHA = .9

#Q Learner model
class qLearner:

    def __init__(self, weights, heuristics, gamma=0.9, learning_rate = 0.2):
        self.weights = weights
        self.heuristics = heuristics
        self.gamma = gamma
        self.lr = learning_rate
        self.possibleMoves = []

    def best_move(self, world, character):
        availableMoves = self.getAvailableMoves(world, character)
        best_q = -math.inf
        best_action = None

        for move in availableMoves:
            #generate new world
            new_world = SensedWorld.from_world(world)

            #check if character is still alive
            if new_world.me(character) is None:
                break

            #make move
            if move[2] == 1:
                new_world.me(character).place_bomb()
            new_world.me(character).move(move[0], move[1])
            new_world, events = new_world.next()

            #check if character is dead and why
            q = 0
            for event in events:
                # check what type of event
                if event.tpe == Event.BOMB_HIT_CHARACTER or event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                    q = -99999
                elif event.tpe == Event.CHARACTER_FOUND_EXIT:
                    q = 99999
            if q == 0:
                q = self.approximate_Q_value(new_world, new_world.me(character))

            if q >= best_q:
                best_q = q
                best_action = move

        return best_action, best_q


    def updateWeights(self, oldWorld, newWorld, character, reward):
        print("Updating")
        if newWorld.me(character) is not None:
            aQv = self.approximate_Q_value(newWorld, newWorld.me(character))
        else:
            aQv = 0

        delta = (reward + self.gamma*aQv)-self.approximate_Q_value(oldWorld, character)

        for i in range(len(self.weights)):
            self.weights[i] += (self.lr * delta * self.heuristics[i](oldWorld, character))

    def getAvailableMoves(self, wrld, char):
        """ Generate a list of possible coordinates to move to """
        # PARAM [world.World] wrld: the world which we want to search
        # PARAM [tuple of (int,int)] current: the current coordinate
        # RETURN [list of node.Node]: A list of node possible nodes to move to

        moves = []
        current = (char.x, char.y)

        # Go through the possible 8-moves
        #
        # Loop through delta x
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (current[0] + dx >= 0) and (current[0] + dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the character is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (current[1] + dy >= 0) and (current[1] + dy < wrld.height()):
                            # No need to check impossible moves
                            if wrld.empty_at(current[0]+dx, current[1]+dy) or wrld.exit_at(current[0]+dx, current[1]+dy):
                                if len(wrld.bombs) == 0:
                                    moves.append((dx, dy, 1))
                                moves.append((dx, dy, 0))

        return moves

    def approximate_Q_value(self, world, character):
        """ Calculate the approximate Q value """
        # PARAM [world.World] wrld: the world current world
        # PARAM [entity.CharacterEntity] char: a character entity
        # RETURN [float]: the approximate Q value
        sum = 0
        for i in range(len(self.heuristics)):
            sum += self.weights[i]*self.heuristics[i](world, character)
        return sum


