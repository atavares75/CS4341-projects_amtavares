import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        util, move = self.min_max(brd, alpha=float("-inf"), beta=float("inf"), depth=1, maximizer=True)
        return move


    # Runs min_max with alpha beta pruning
    #
    # PARAM [board.Board] brd: the current board state
    # PARAM [int] alpha: best value of maximizer
    # PARAM [int] best: best value of minimizer
    # PARAM [int] depth: depth of the search
    # PARAM [boolean] player_turn: True if agent's turn, False otherwise
    # RETURN [int]: token where the token must be added
    def min_max(self, brd, alpha, beta, depth, maximizer):

        if brd.get_outcome() > 0 or depth == self.max_depth:
            return self.score(brd), 0

        best = -math.inf if maximizer else math.inf
        move = None

        succ = self.get_successors(brd)
        for new_state, col in succ:
            util, c = self.min_max(new_state, alpha, beta, depth+1, not maximizer)
            if maximizer and best <= util:
                best = util
                move = col
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
            if (not maximizer) and best >= util:
                best = util
                move = col
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best, move


    # Returns utility value for board state
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [float]: utility value of board
    def score(self, brd):
        score = 0
        score_h = self.check_direction(brd, 1, 0)  # Horizontal
        if score_h == math.inf or score_h == -math.inf: return score_h

        score_v = self.check_direction(brd, 0, 1)  # Vertical
        if score_v == math.inf or score_v == -math.inf: return score_v

        score_d = self.check_direction(brd, 1, 1)  # Diagonal up
        if score_d == math.inf or score_d == -math.inf: return score_d

        score_d1 = self.check_direction(brd, 1, -1) # Diagonal down
        if score_d1 == math.inf or score_d1 == -math.inf: return score_d1

        return score_h + score_v + score_d + score_d1

    def check_direction(self, brd, dx, dy):
        score = 0
        for x in range(brd.w):
            for y in range(brd.h):
                temp = self.evaluate(brd, x, y, dx, dy)
                if temp == math.inf or temp == -math.inf: return temp
                score += temp
        return score

    # Evaluation function
    #
    # PARAM [int] x:  the x coordinate of the starting cell
    # PARAM [int] y:  the y coordinate of the starting cell
    # PARAM [int] dx: the step in the x direction
    # PARAM [int] dy: the step in the y direction
    # RETURN [float]: score of the state
    def evaluate(self, brd, x, y, dx, dy):
        """Return True if a line of identical tokens exists starting at (x,y) in direction (dx,dy)"""
        # Avoid out-of-bounds errors
        if ((x + (brd.n - 1) * dx >= brd.w) or
                (y + (brd.n - 1) * dy < 0) or (y + (brd.n - 1) * dy >= brd.h)):
            return 0.0
        # Get token at (x,y)
        t = brd.board[y][x]
        if t == 0:
            return 0
        score = 1.0

        # win_pos = set()

        # Go through elements
        for i in range(1, brd.n):
            if brd.board[y + i * dy][x + i * dx] == t:
                score += 1.0
                # if score == brd.n-1 and t == self.player: # next position wins
                #     if win_pos.add((y,x))

            elif brd.board[y + i * dy][x + i * dx] > 0:
                return 0.0

        # Check auto wins
        if score == 2 and t != self.player:
            score += self.check_win_auto(brd, x, y, dx, dy)

        if score == brd.n and t == self.player:
            return math.inf
        elif score == brd.n and t != self.player:
            return -math.inf

        if t != self.player:
            score = -1*score

        return score


    def check_win_auto(self, brd, x, y, dx, dy):
        # If position before is in bounds
        if not (-1 < (x * -dx) < brd.h and -1 < (y * -dy) < brd.w):
            return 0

        if brd.board[y * -dy][x * -dx] != 0: # Previous slot in line is occupied
            return 0

        else: # Previous slot in line is free
            return -math.inf


    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
