# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back


class Node:
    """
    A node class for A* Search
    parent is the parent of the current node
    position is the position of the current node
    g is the cost from start to current node
    h is the heutristic
    f is total cost of present node

    """

    def __init__(self, position, parent=None,):
        self.position = position
        self.parent = parent
        self.x = position[0]
        self.y = position[1]

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.pos() == other.pos()
        return False

    def __hash__(self):
        return hash(((self.x+1)**2) * ((self.y+1)**2))

    def __lt__(self, other):
        return self.f < other.f

    def pos(self):
        return self.x, self.y

    def set_ghf(self, g, h):
        self.g = g
        self.h = h
        self.f = g+h
