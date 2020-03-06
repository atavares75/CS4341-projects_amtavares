import heapq
import math


def find_bombs(wrld):
    """ Find the coordinates of all bombs """
    # PARAM [world.World] wrld: the world which we want to search
    # RETURN [list of (int, int)]: coordinates of all bombs in the world

    bombs = []
    for x in range(0, wrld.width()):
        for y in range(0, wrld.height()):
            if wrld.bomb_at(x,y):
                bombs.append(x,y)

    return bombs


def find_explosions(wrld):
    """ Find the coordinates of any explosions """
    # PARAM [world.World] wrld: the world which we want to search
    # RETURN [list of (int, int)]: coordinates of all explosions in the world

    explosions = []
    for x in range(0, wrld.width()):
        for y in range(0, wrld.height()):
            if wrld.exit_at(x, y):
                explosions.append(x, y)

    return explosions


def find_exits(wrld):
    """ Find the coordinates of any exits """
    # PARAM [world.World] wrld: the world which we want to search
    # RETURN [list of (int, int)]: coordinates of all exits in the world

    exits = []
    for x in range(0, wrld.width()):
        for y in range(0, wrld.height()):
            if wrld.exit_at(x, y):
                exits.append(x, y)

    return exits


def find_monsters(wrld):
    """ Find the coordinates of any monsters """
    # PARAM [world.World] wrld: the world which we want to search
    # RETURN [list of (int, int)]: coordinates of all monsters in the world

    monsters = []
    for x in range(0, wrld.width()):
        for y in range(0, wrld.height()):
            if wrld.exit_at(x, y):
                monsters.append(x, y)

    return monsters


def find_closest_point(origin, points):
    """ Find the closest point in a list of points to an origin point """
    # PARAM [tuple of (int, int)]: the coordinates of the origin point
    # PARAM [list of (int, int)]: a list of coordinates
    # RETURN [tuple of (int,int)]: coordinates of the closest point
    closest = points[0]

    for point in points:
        if diagonal_distance(origin, point) < diagonal_distance(origin, closest):
            closest = point

    return point


def x_distance_to_bomb(wrld, char):
    """ Finds the x component of the distance to the closest bomb """
    # PARAM [world.World] wrld: the world which we want to search
    # PARAM [entity.CharacterEntity] char: a character entity

    # Find bombs in the world
    bombs = find_bombs(wrld)

    if not bombs:
        return math.inf

    closest_bomb = find_closest_point((char.x, char.y), bombs)
    x_dist = abs(char.x - closest_bomb[0])

    return x_dist


def y_distance_to_bomb(wrld, char):
    """ Finds the y component of the distance to the closest bomb """
    # PARAM [world.World] wrld: the world which we want to search
    # PARAM [entity.CharacterEntity] char: a character entity

    # Find bombs in the world
    bombs = find_bombs(wrld)

    if not bombs:
        return math.inf

    closest_bomb = find_closest_point((char.x, char.y), bombs)
    y_dist = abs(char.y - closest_bomb[1])

    return y_dist


def distance_to_closest_monster(wrld, char):
    """ Find the distance to the closest monster """
    # PARAM [world.World] wrld: the world which we want to search
    # PARAM [entity.CharacterEntity] char: a character entity

    mnosters = find_monsters(wrld)

    pass



def distance_to_closest_monster(wrld, char):
    """ Find the distance to the closest monster """
    # PARAM [world.World] wrld: the world which we want to search
    # PARAM [entity.CharacterEntity] char: a character entity

    pass


def distance_to_closest_wall(wrld, char):
    """ Find the distance to the closest wall """
    # PARAM [world.World] wrld: the world which we want to search
    # PARAM [entity.CharacterEntity] char: a character entity

    pass


def diagonal_distance(current, end):
    """" Calculate the heuristic of a given coordinate """
    # PARAM [tuple of (int, int)] current: the current coordinate
    # PARAM [tuple of (int, int)] end: the target coordinate
    # RETURN int: the heuristic for the current coordinate

    # Set D, the cost to move horizontally or vertically, and D2, the cost to move diagonally
    D = D2 = 1

    # Find horizontal distance to the target coordinate, dx, and vertical distance to the target coordinate, dy
    dx = abs(current[0] - end[0])
    dy = abs(current[1] - end[1])

    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)


def get_neighbors(wrld, current):
    """ Generate a list of possible coordinates to move to """
    # PARAM [world.World] wrld: the world which we want to search
    # PARAM [tuple of (int,int)] current: the current coordinate
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
    # PARAM [list of (int, int)] path: the path of coordinates to the end goal.
    # RETURN [list of (int,int)] movelist: list of tuples (dx,dy) corresponding to the direction of movement to the
    #                                      next coordinate in the path

    movelist = []
    for i in range(1, len(path)):
        dx = path[i][0] - path[i - 1][0]
        dy = path[i][1] - path[i - 1][1]
        movelist.append((dx, dy))

    return movelist


def aStarSearch(wrld, start, end):
    """ Perform the search for the A* algorithm """
    # PARAM [world.World] wrld: the world which we want to search
    # RETURN [list of (int, int)]: a list of coordinates leading to the target node

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

    # Create the path in reverse order
    while current != start:
        rev_path.append(current)
        current = came_from[current]

    # Reverse the path
    rev_path.append(current)
    path = rev_path[::-1]

    return path


def get_movelist(wrld, start, end):
    """ Generate a movelist from on point to another """
    # PARAM [world.World] wrld: the world which we want to search
    # PARAM [tuple of (int,int)] start: coordinates of the start point
    # PARAM [tuple of (int,int)] end: coordinates of the end point

    # Find the path from start to end
    path = aStarSearch(wrld, start, end)
    return movelist_from_path(path)
