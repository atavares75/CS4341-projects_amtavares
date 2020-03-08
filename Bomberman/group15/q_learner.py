# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')

from f_functions import *
from events import Event
from sensed_world import SensedWorld

# Training Values
GAMMA = .9
ALPHA = .2

#Q Learner model
class qLearner:

    def __init__(self, functions,  weights=[], bombs=True):
        if weights:
            self.weights = weights
        else:
            self.weights = [0 for _ in range(len(functions))]

        self.functions = functions
        self.bombs = bombs
        self.pos = None
        self.move = None

    def get_possible_moves(self, wrld, current):
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
                            if self.bombs:
                                moves.append((current[0] + dx, current[1] + dy, 1))

                            moves.append((current[0] + dx, current[1] + dy, 0))

        return moves

    def best_move(self, wrld, char):
        max_q_score = -10000
        max_action = (0, 0, 0)

        for move in self.get_possible_moves(wrld, (char.x, char.y)):
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

    def update_weights(self, new_wrld, char, reward):
        """ Update weights for qLearner """
        delta = reward - self.approximate_Q_value(new_wrld, char)

        for i in range(len(self.weights)):
            self.weights[i] += ALPHA * delta * self.functions[i](new_wrld, char)

    def approximate_Q_value(self, wrld, char):
        """ Calculate the approximate Q value """
        # PARAM [world.World] wrld: the world current world
        # PARAM [entity.CharacterEntity] char: a character entity
        # RETURN [float]: the approximate Q value
        total = 0

        for i in range(len(self.functions)):
            total += self.weights[i] * self.functions[i](wrld, char)

        return total


