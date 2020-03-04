# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back
from node import Node
import heapq


class TestCharacter(CharacterEntity):
    def __init__(self, name, avatar, x, y):
        CharacterEntity.__init__(self, name, avatar, x, y)

        self.need_search = True
        self.movelist = []

    def do(self, wrld):
        # Your code here
        if self.need_search:
            self.astar(wrld)
            self.need_search = False

        dx, dy = self.movelist.pop()
        self.move(dx, dy)


    def asearch(self, wrld):
        """ Perform the search for the A* algorithm """
        # PARAM [world.World] wrld: the world which we want to search
        # RETRUN [list of node.Node]: a list of nodes leading to the target node

        def heuristic():
            """" Calculate the heuristic of a given node """
            # PARAM [node.Node] current: the current node
            # PARAM [noe.Node] end: the target node
            # RETRUN int: the hueristic for the current node

            # Set D, the cost to move horizontally or vertically, and D2, the cost to move diagonally
            D = D2 = 1

            # Find horizantal distance to the target node, dx, and vertical distance to the target node, dy
            dx = abs(current.x - end.x)
            dy = abs(current.y - end.y)

            return D * (dx + dy) + (D2 - 2*D) * min(dx, dy)

        def get_neighbors():
            """ Generate a list of possible nodes to move to """
            # PARAM [world.World] wrld: the world which we want to search
            # PARAM [node.Node] current: the current node
            # RETURN [list of node.Node]: A list of node possible nodes to move to

            neighbors = []

            # Go through the possible 8-moves
            #
            # Loop through delta x
            for dx in [-1, 0, 1]:
                # Avoid out-of-bound indexing
                if (current.x + dx >= 0) and (current.x + dx < wrld.width()):
                    # Loop through delta y
                    for dy in [-1, 0, 1]:
                        # Make sure the monster is moving
                        if (dx != 0) or (dy != 0):
                            # Avoid out-of-bound indexing
                            if (current.y + dy >= 0) and (current.y + dy < wrld.height()):
                                # No need to check impossible moves

                                # Make a node for the new position and add it to the list of neighbors
                                temp_node = Node((current.x + dx, current.y + dy), current)
                                neighbors.append(temp_node)

            return neighbors

        me = wrld.me(self)

        max_iters = wrld.time
        total_iters = 0

        came_from = {}
        cost_so_far = {}
        priorq = []
        rev_path = []

        # Che cost to make a move
        cost_of_move = 1

        # Make start node and end node
        start = Node((me.x, me.y), None)
        start.set_ghf(0, 0)
        end = Node((wrld.exitcell[0], wrld.exitcell[1]), None)

        came_from[start] = None
        cost_so_far[start] = 0


        # Add start to priority queue
        heapq.heappush(priorq, (start.f, start))

        while priorq:
            # Increment iteration count
            total_iters += 1

            # Check that you haven't exceeded max iterations
            if total_iters > max_iters:
                print("Stopping search, maximum iteration reached")
                break

            current = heapq.heappop(priorq)[1]

            # If current node is target node
            if current == end:
                break

            # Loop through possible neighbors
            for neighbor in get_neighbors():
                if not wrld.wall_at(neighbor.x, neighbor.y):
                    new_cost = cost_so_far[current] + cost_of_move
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost

                        # Set values of g, h, and f for node
                        neighbor.set_ghf(new_cost, heuristic())

                        heapq.heappush(priorq, (neighbor.f, neighbor))
                        came_from[neighbor] = current

        while current is not None:
            rev_path.append(current.pos())
            current = current.parent

        path = rev_path[::-1]

        return path


    def movelist_from_path(self, path):
        """ Produce a movelist from the given path """
        # PARAM [list of node.Nodes] path: the path of nodes to the end goal.
        # RETURN [list of (int,int)] movelist: list of tuples (dx,dy) corresponding to the direction of movement to the
        #                                      next node in the path

        print(path)
        for i in range(1, len(path)):
            dx = path[i][0] - path[i-1][0]
            dy = path[i][1] - path[i-1][1]
            self.movelist.append((dx, dy))

    def astar(self, wrld):
        path = self.asearch(wrld)
        self.movelist_from_path(path)
