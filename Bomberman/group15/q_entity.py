import sys

sys.path.insert(0, '../bomberman')
from entity import CharacterEntity
from sensed_world import SensedWorld

class qEntity(CharacterEntity):

    def __init__(self, name, avatar, x, y, qLearner, iterNum, maxIterations, bombs = True, trainModel=False):
        CharacterEntity.__init__(name, avatar, x, y)
        #Includes other variables needed for q learning
        self.qLearner = qLearner
        self.trainModel = trainModel
        self.iterNum = iterNum
        self.maxIterations = maxIterations
        self.bombs = bombs

    def do(self):
        if self.trainModel:
            pass
        else:
            pass

    #updates weights
    def done(self):
        pass


