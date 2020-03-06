# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from f_functions import *
import heapq


class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)

        self.need_search = True
        self.movelist = []

    def do(self, wrld):
        # Your code here
        if self.need_search:
            movelist = get_movelist(wrld, (wrld.me(self).x, wrld.me(self).y), wrld.exitcell)
            self.movelist = movelist
            self.need_search = False

        dx, dy = self.movelist.pop()
        self.move(dx, dy)


