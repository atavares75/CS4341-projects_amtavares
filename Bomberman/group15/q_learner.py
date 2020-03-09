# This is necessary to find the main code
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
        availableMoves = self.getAvailableMoves(world, (character.x, character.y))
        best_q = -9999
        best_action = (0,0,0)

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
                if event.tpe == Event.BOMB_HIT_CHARACTER:
                    q = -9999
                    break
                if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                    q = -9999
                    break
                if event.tpe == Event.CHARACTER_FOUND_EXIT:
                    q = 9999
                    break
            if q == 0:
                q = self.approximate_Q_value(new_world, new_world.me(character))

            if q >= best_q:
                best_q = q
                best_action = move

        return best_q, best_action



    def updateWeights(self, oldWorld, newWorld, character, reward):
        if newWorld.me(character) is not None:
            aQv = self.approximate_Q_value(newWorld, newWorld.me(character))
        else:
            aQv = 0
        delta = (reward + self.gamma*aQv)-self.approximate_Q_value(oldWorld, character)
        print("updating")
        for i in range(len(self.weights)):
            self.weights[i] += (self.lr * delta * self.heuristics[i](oldWorld, character))

    def get_possible_moves(self, wrld, char):
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
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (current[1] + dy >= 0) and (current[1] + dy < wrld.height()):
                            # No need to check impossible moves
                            if wrld.empty_at(current[0]+dx, current[1]+dy) or wrld.exit_at(current[0]+dx, current[1]+dy):
                                if len(wrld.bombs) == 0:
                                    moves.append((current[0] + dx, current[1] + dy, 1))
                                moves.append((current[0] + dx, current[1] + dy, 0))

        return moves

    def best_move(self, wrld, char):
        max_q_score = -9999
        max_action = (0, 0, 0)

        for move in self.get_possible_moves(wrld, char):
            new_world = SensedWorld.from_world(wrld)

            if new_world.me(char) is None:
                continue

            new_world.me(char).move(move[0], move[1])
            if move[2] != 0:
                new_world.me(char).place_bomb()

            new_world, events = new_world.next()

            if new_world.me(char) is None:
                for event in events:
                    if event.tpe == Event.CHARACTER_KILLED_BY_MONSTER or event.tpe == Event.BOMB_HIT_CHARACTER:
                        q = -9999

                    if event.tpe == Event.CHARACTER_FOUND_EXIT:
                        q = 9999

            else:
                q = self.approximate_Q_value(new_world, new_world.me(char))

            if q > max_q_score:
                max_q_score = q
                max_action = move

        return max_action, max_q_score

    def approximate_Q_value(self, world, character):
        """ Calculate the approximate Q value """
        # PARAM [world.World] wrld: the world current world
        # PARAM [entity.CharacterEntity] char: a character entity
        # RETURN [float]: the approximate Q value
        sum = 0
        for i in range(len(self.heuristics)):
            sum += self.weights[i]*self.heuristics[i](world, world.me(character))
        return sum


