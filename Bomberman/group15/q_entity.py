import sys

sys.path.insert(0, '../bomberman')
from entity import CharacterEntity
from sensed_world import SensedWorld

class qEntity(CharacterEntity):

    def __init__(self):
        CharacterEntity.__init__()
        #Includes other variables needed for q learning

    def do(self):
        pass

    def updateWeights(self):
        pass


