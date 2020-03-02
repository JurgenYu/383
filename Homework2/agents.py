import random
import math


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def get_move(self, state, depth=None):
        possibles = [ m for m, v in state.successors() ]
        return random.choice(possibles)


class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = int(input(prompt))
        return move, move__state[move]


class ComputerAgent:
    """Artificially intelligent agent that uses minimax to select the best move."""

    def get_move(self, state, depth=None):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state, depth)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state, depth):
        """Determine the minimax utility value the given state.

        Args:
            state: a connect4.GameState object representing the current board
            depth: the maximum depth of the game tree that minimax should traverse before
                estimating the utility using the evaluation() function.  If depth is 0, no
                traversal is performed, and minimax returns the results of a call to evaluation().
                If depth is None, the entire game tree is traversed.

        Returns: the minimax utility value of the state
        """
        #
        #value = []
        value = 0
        if depth is None:
            depth = -1
        winner = state.winner()
        if winner is not None:
            return 100 if winner > 0 else -100
        if depth == 0:
            return self.evaluation(state)
        else:
            for each in state.successors():
                value+=self.minimax(each[1], depth - 1)
                 # value.sort(key = lambda x: x if x > 0 else -x, reverse = True)
        return value # Change this line!

    def evaluation(self, state): #zzz must be O(1)
        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in O(1) time!

        Args:
            state: a connect4.GameState object representing the current board

        Returns: a heusristic estimate of the utility value of the state
        """
        #
        value = 0
        for r in range(state.num_rows):
            for c in range(state.num_cols - state.num_win + 1):
                # print("r {}, c {}".format(r, c))
                # print(list(range(c, c+state.num_win)))
                tmpx = state.board[r][c]
                count = 0
                for x in range(c, c+state.num_win):
                    if state.board[r][x] == tmpx:
                        count += tmpx
                    else:
                        tmpx = state.board[r][x]
                        count = 0
                    if abs(count) > value:
                        value = count

        # check verticals
        for c in range(state.num_cols):
            for r in range(state.num_rows - state.num_win + 1):
                tmpy = state.board[r][c]
                count = 0
                for y in range(r, r+state.num_win):
                    if state.board[y][c] == tmpy:
                        count += tmpy
                    else:
                        tmpy = state.board[y][c]
                        count = 0
                    if abs(count) > value:
                        value = count

        # check diags
        for r in range(state.num_rows):
            for c in range(state.num_cols):
                if state.board[r][c] == 0:
                    continue
                # Checks positive slope diagonals
                tmpp = state.board[r][c]
                count  = 0
                if r + 3 < state.num_rows and c + 3 < state.num_cols:
                    for i in range(1, 4):
                        if state.board[r + i][c + i] == tmpp:
                            count += tmpp
                        else: 
                            tmpp = state.board[r + i][c + i]
                            count = 0
                        if abs(count) > value:
                            value = count if tmpp > 0 else -count
                # Checks negative slope diagonals
                tmpn = state.board[r][c]
                count  = 0
                if r + 3 < state.num_rows and c >= 3:
                    for i in range(1, 4):
                        if state.board[r + i][c - i] == tmpn:
                            count += tmpn
                        else:
                            tmpn = state.board[r + i][c - i]
                            count  = 0
                        if abs(count) > value:
                            value = count if tmpn > 0 else -count
        #
        nwin = float(state.num_win)
        returnval = value / nwin
        return returnval # Change this line!


class ComputerPruneAgent(ComputerAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move."""

    def minimax(self, state, depth):
        util, pruned = self.minimax_prune(state, depth)
        return util

    def minimax_prune(self, state, depth):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: see ComputerAgent.minimax() above

        Returns: the minimax utility value of the state, along with a list of state objects that
            were not expanded due to pruning.
        """
        #
        # Fill this in!
        #
        return 44, []  # Change this line!


