def boardFromFile(filename):
    with open(filename, "r") as f:
        board = []
        for line in f:
            row = [int(n) for n in line.split('\t')]
            board.append(row)
        return board

class GameState(object):
    def __init__(self, board, turn=1, state=None):
        self.board = board
        if state is None:
            self.state = [[0 for col in board] for row in board]
        else:
            self.state = state
        self.turn = 1

    def calculateScores(self):
        # returns (maximizing Player's score, minimizing Player's score)
        maxPlayerScore = 0
        minPlayerScore = 0
        for r, row in enumerate(self.board):
            for c, n in enumerate(row):
                if self.state[r][c] == 1:
                    maxPlayerScore += n
                elif self.state[r][c] == -1:
                    minPlayerScore += n
        return (maxPlayerScore, minPlayerScore)

    def calculateScore(self):
        # returns difference between maxPlayer's score and minPlayer's score
        # maxPlayer is winning if return value is positive
        # minPlayer is winning if return value is negative
        maxPlayerScore, minPlayerScore = self.calculateScores()
        return maxPlayerScore - minPlayerScore

    def findNextStates(self):
        nextStates = []
        for r, row in enumerate(self.state):
            for c, st in enumerate(row):
                # first check for airdrop
                if st == 0:
                    nextStates.append(self.airdrop(r, c))
                # then check for blitz
                if self.checkAdjacent(r, c):
                    nextStates.append(self.blitz(r, c))
        return nextStates

    def checkAdjacent(self, row, col):
        # helper function that checks if self.turn is present in adjacent tiles
        for r in (row-1, row+1):
            if r >= 0 and r < len(self.state):
                if self.state[r][col] == self.turn:
                    return True
        for c in (col-1, col+1):
            if c >= 0 and c < len(self.state[row]):
                if self.state[row][c] == self.turn:
                    return True
        return False

    def airdrop(self, row, col):
        # must check beforehand if (row, col) is already occupied
        newState = [x[:] for x in self.state]
        newState[row][col] = self.turn
        return GameState(self.board, -self.turn, newState)

    def blitz(self, row, col):
        # must check beforehand if (row, col) is adjacent to occupied
        newState = [x[:] for x in self.state]
        newState[row][col] = self.turn
        # check if adjacent enemy tiles
        for r in (row-1, row+1):
            if r >= 0 and r < len(newState):
                if newState[r][col] == -self.turn:
                    newState[r][col] = self.turn
        for c in (col-1, col+1):
            if c >= 0 and c < len(newState[row]):
                if newState[row][c] == -self.turn:
                    newState[row][c] = self.turn
        return GameState(self.board, -self.turn, newState)

    def minimax(self, depth=3):
        # perform a minimax tree search from this state
        if depth <= 0:
            return self.calculateScore()
        nextStates = self.findNextStates()
        if len(nextStates) == 0:
            return self.calculateScore()
        if self.turn == 1:
            # maximizing
            compare = max
        elif self.turn == -1:
            # minimizing
            compare = min
        else:
            raise ValueError("self.turn is invalid: {0}".format(self.turn))
        bestVal = None
        for nextState in nextStates:
            val = nextState.minimax(depth-1)
            if bestVal is None:
                bestVal = val
            else:
                bestVal = compare(bestVal, val)
        return bestVal

if __name__ == "__main__":
    board = boardFromFile("Westerplatte.txt")
    initState = GameState(board)
    print initState.minimax()
