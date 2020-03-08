sys.path.insert(0, '../bomberman')
from entity import CharacterEntity
from sensed_world import SensedWorld

#Q Learner model
class qLearner:

    def __init__(self, weights, heuristics, gamma=0.9, learning_rate = 0.2):
        self.weights = weights
        self.heuristics = heuristics
        self.gamma = gamma
        self.lr = learning_rate
        self.possibleMoves = []

    def getAvailableMoves(self, world, character):
        pass

    def best_move(self, world, character):
        availableMoves = self.getAvailableMoves(world, character)
        best_q = -9999
        best_action = (0,0,0)

        for move in availableMoves:
            #generate new world
            new_world = SensedWorld.from_world(world)

            #check if character is still alive
            if new_world.me(character) is None:
                break

            #make move
            new_world.me(character).move(move[0], move[1])
            if move[3] == 1:
                new_world.me(character).place_bomb()
            new_world, events = new_world.next()

            #check if character is dead and why
            if new_world.me(character) is None:
                for event in events:
                    # check what type of event
                    pass





    def updateWeights(self, oldWorld, newWorld, character, reward):
        delta = (reward + self.gamma*self.approximate_Q_value(newWorld))-self.approximate_Q_value(oldWorld)

        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + self.lr*delta*self.heuristics[i](oldWorld, character)


    def approximate_Q_value(self, world, character):
        sum = 0

        for i in range(len(self.heuristics)):
            sum += self.weights[i]*self.heuristics[i](world, character)

        return sum

