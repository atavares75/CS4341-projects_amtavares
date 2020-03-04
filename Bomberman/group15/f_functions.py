import heapq


def diagonal_distance(current, end):
    """" Calculate the heuristic of a given node """
    # PARAM [node.Node] current: the current node
    # PARAM [noe.Node] end: the target node
    # RETRUN int: the hueristic for the current node

    # Set D, the cost to move horizontally or vertically, and D2, the cost to move diagonally
    D = D2 = 1

    # Find horizantal distance to the target node, dx, and vertical distance to the target node, dy
    dx = abs(current[0] - end[0])
    dy = abs(current[1] - end[1])

    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


def get_neighbors(wrld, current):
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
        if (current[0] + dx >= 0) and (current[0] + dx < wrld.width()):
            # Loop through delta y
            for dy in [-1, 0, 1]:
                # Make sure the monster is moving
                if (dx != 0) or (dy != 0):
                    # Avoid out-of-bound indexing
                    if (current[1] + dy >= 0) and (current[1] + dy < wrld.height()):
                        # No need to check impossible moves
                        neighbors.append((current[0] + dx, current[1] + dy))

    return neighbors


def movelist_from_path(path):
    """ Produce a movelist from the given path """
    # PARAM [list of node.Nodes] path: the path of nodes to the end goal.
    # RETURN [list of (int,int)] movelist: list of tuples (dx,dy) corresponding to the direction of movement to the
    #                                      next node in the path

    movelist = []
    for i in range(1, len(path)):
        dx = path[i][0] - path[i - 1][0]
        dy = path[i][1] - path[i - 1][1]
        movelist.append((dx, dy))

    return movelist


def aStarSearch(wrld, start, end):
    """ Perform the search for the A* algorithm """
    # PARAM [world.World] wrld: the world which we want to search
    # RETURN [list of node.Node]: a list of nodes leading to the target node

    max_iters = wrld.time
    total_iters = 0

    came_from = {}
    cost_so_far = {}
    frontier = []
    rev_path = []

    # set cost to make a move
    cost_of_move = 1

    came_from[start] = None
    cost_so_far[start] = 0

    # Add start to priority queue
    heapq.heappush(frontier, (0, start))

    while frontier:
        # Increment iteration count
        total_iters += 1

        # Check that you haven't exceeded max iterations
        if total_iters > max_iters:
            print("Stopping search, maximum iteration reached")
            break

        current = heapq.heappop(frontier)[1]

        # If the current position in the end goal
        if current == end:
            break

        # Loop through possible neighbors
        for neighbor in get_neighbors(wrld, current):
            if not wrld.wall_at(neighbor[0], neighbor[1]):
                new_cost = cost_so_far[current] + cost_of_move
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    prioirty = new_cost + diagonal_distance(current, end)
                    heapq.heappush(frontier, (prioirty, neighbor))
                    came_from[neighbor] = current

    while current != start:
        rev_path.append(current)
        current = came_from[current]

    rev_path.append(current)
    path = rev_path[::-1]

    return path


def get_movelist(wrld, start, end):
    path = aStarSearch(wrld, start, end)
    return movelist_from_path(path)