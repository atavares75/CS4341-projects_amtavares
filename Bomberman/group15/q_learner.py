
# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')

from f_functions import *
from events import Event
from sensed_world import SensedWorld


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
        reward = 0

        for move in availableMoves:
            #generate new world
            new_world = SensedWorld.from_world(world)

            #check if character is still alive
            if new_world.me(character) is None:
                break

            #make move
            new_world.me(character).move(move[0], move[1])
            if move[2] == 1:
                new_world.me(character).place_bomb()
            new_world, events = new_world.next()

            #check if character is dead and why
            if new_world.me(character) is None:
                for event in events:
                    # check what type of event
                    if event.tpe == Event.BOMB_HIT_CHARACTER or event.tpe == Event.CHARACTER_KILLED_BY_MONSTER:
                        q = 0
                        reward = -9999
                    if event.tpe == Event.CHARACTER_FOUND_EXIT:
                        q = 0
                        reward = 9999
            else:
                q = self.approximate_Q_value(new_world, new_world.me(character))

            if q > best_q:
                best_q = q
                best_action = move

        return best_q, best_action, reward



    def updateWeights(self, oldWorld, newWorld, character, reward):
        delta = (reward + self.gamma*self.approximate_Q_value(newWorld, character))
        delta = delta-self.approximate_Q_value(oldWorld, character)

        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + self.lr*delta*self.heuristics[i](newWorld, character)


    def getAvailableMoves(self, wrld, current):
        """ Generate a list of possible coordinates to move to """
        # PARAM [world.World] wrld: the world which we want to search
        # PARAM [tuple of (int,int)] current: the current coordinate
        # RETURN [list of node.Node]: A list of node possible nodes to move to

        moves = []

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
                            moves.append((current[0] + dx, current[1] + dy, 1))
                            moves.append((current[0] + dx, current[1] + dy, 0))

        return moves


    def approximate_Q_value(self, world, character):
        sum = 0
        for i in range(len(self.heuristics)):
            sum += self.weights[i]*self.heuristics[i](world, character)

        return sum

