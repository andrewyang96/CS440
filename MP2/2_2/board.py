def boardFromFile(filename):
    with open(filename, "r") as f:
        board = []
        for line in f:
            row = [int(n) for n in line.split('\t')]
            board.append(row)
        return board

class GameState(object):
    def __init__(self, board, turn=1):
        self.board = board
        self.state = [[0 for col in board] for row in board]
        self.turn = 1

    def calculateScore():
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

    def findNextStates():
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

    def checkAdjacent(row, col):
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

    def airdrop(row, col):
        # must check beforehand if (row, col) is already occupied
        newState = [row[:] for row in self.state]
        newState[row][col] = self.turn
        return Board(self.board, newState, -self.turn)

    def blitz(row, col):
        # must check beforehand if (row, col) is adjacent to occupied
        newState = [row[:] for row in self.state]
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
        return Board(self.board, newState, -self.turn)
