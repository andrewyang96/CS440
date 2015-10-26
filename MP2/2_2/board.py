import time
import os

# Redirect stdout
import sys
from contextlib import contextmanager
@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout

def boardFromFile(filename):
    with open(filename, "r") as f:
        board = []
        for line in f:
            row = [int(n) for n in line.split('\t')]
            board.append(row)
        return board

class Counter(object):
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
    def __str__(self):
        return str(self.count)
    def __repr__(self):
        return self.count

class GameState(object):
    def __init__(self, board, turn=1, state=None):
        self.board = board
        if state is None:
            self.state = [[0 for col in board] for row in board]
        else:
            self.state = state
        self.turn = turn

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.letterRepr()])

    def printBoard(self):
        print "\n".join([" ".join(row) for row in self.board])

    def letterRepr(self):
        ret = []
        for row in self.state:
            retRow = []
            for tile in row:
                if tile == 1:
                    retRow.append("F")
                elif tile == -1:
                    retRow.append("S")
                else:
                    retRow.append("O")
            ret.append(retRow)
        return ret

    def isFull(self):
        for row in self.state:
            for tile in row:
                if tile == 0:
                    return False
        return True

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
        # also space must be empty
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

    def minimax(self, depth=3, counter=None):
        # perform a minimax tree search from this state
        if counter is not None:
            counter.increment()
        if depth <= 0:
            return (self.calculateScore(), self.state)
        nextStates = self.findNextStates()
        if len(nextStates) == 0:
            return (self.calculateScore(), self.state)
        if self.turn == 1:
            # maximizing
            compare = max
        elif self.turn == -1:
            # minimizing
            compare = min
        else:
            raise ValueError("self.turn is invalid: {0}".format(self.turn))
        bestVal = None
        bestState = None
        for nextState in nextStates:
            val = nextState.minimax(depth-1, counter)[0]
            if bestVal is None:
                bestVal = val
                bestState = nextState
            else:
                if compare(bestVal, val) != bestVal:
                    bestVal = val
                    bestState = nextState
        return (bestVal, bestState)

    def alphabeta(self, depth=5, alpha=None, beta=None, counter=None):
        # perform an alpha-beta tree search from this state
        if counter is not None:
            counter.increment()
        if depth <= 0:
            return (self.calculateScore(), self.state)
        nextStates = self.findNextStates()
        if len(nextStates) == 0:
            return (self.calculateScore(), self.state)
        if self.turn == 1:
            # maximizing
            compare = max
        elif self.turn == -1:
            compare = min
        else:
            raise ValueError("self.turn is invalid: {0}".format(self.turn))
        val = None
        bestState = None
        for nextState in nextStates:
            if val is None:
                val = nextState.alphabeta(depth-1, alpha, beta, counter)[0]
                bestState = nextState
            else:
                newVal = nextState.alphabeta(depth-1, alpha, beta, counter)[0]
                if compare(val, newVal) != val:
                    val = newVal
                    bestState = nextState
            if self.turn == 1:
                if alpha is None:
                    alpha = val
                else:
                    alpha = max(alpha, val)
            else: # self.turn == -1
                if beta is None:
                    beta = val
                else:
                    beta = min(beta, val)
            if alpha is not None and beta is not None and beta <= alpha:
                break # beta cut-off
        return (val, bestState)

def playGame(maxUseAlphabeta=True, minUseAlphabeta=True, minimaxDepth=3, alphabetaDepth=5, counter=None):
    # allow mix of minimax and alpha-beta pruning
    currState = GameState(board)
    turnNum = 1
    while not currState.isFull():
        counter = Counter()
        playMove = None
        print "Turn", turnNum
        print >> sys.stderr, "Turn", turnNum
        if currState.turn == 1:
            if maxUseAlphabeta:
                print "Player 1 using Alphabeta"
                print >> sys.stderr, "Player 1 using Alphabeta"
                playMove = lambda counter: currState.alphabeta(depth=alphabetaDepth, counter=counter)
            else:
                print "Player 1 using Minimax"
                print >> sys.stderr, "Player 1 using Minimax"
                playMove = lambda counter: currState.minimax(depth=minimaxDepth, counter=counter)
        else:
            if minUseAlphabeta:
                print "Player 2 using Alphabeta"
                print >> sys.stderr, "Player 2 using Alphabeta"
                playMove = lambda counter: currState.alphabeta(depth=alphabetaDepth, counter=counter)
            else:
                print "Player 2 using Minimax"
                print >> sys.stderr, "Player 2 using Minimax"
                playMove = lambda counter: currState.minimax(depth=minimaxDepth, counter=counter)
        startTime = time.clock()
        bestHeur, nextState = playMove(counter)
        elapsed = time.clock() - startTime
        print "Best Heuristic:", bestHeur
        print >> sys.stderr, "Best Heuristic:", bestHeur
        print "Nodes Expanded:", counter
        print >> sys.stderr, "Nodes Expanded:", counter
        print "Time Taken:", elapsed
        print >> sys.stderr, "Time Taken:", elapsed
        print "Best Next State:"
        print nextState
        print >> sys.stderr, "Best Next State:"
        print >> sys.stderr, nextState
        print
        currState = nextState
        turnNum += 1
    print "Done!"
    print >> sys.stderr, "Done!"

if __name__ == "__main__":
    if not os.path.exists("results"):
        os.mkdir("results")
    boards = ["Keren.txt", "Narvik.txt", "Sevastopol.txt", "Smolensk.txt", "Westerplatte.txt"]
    # boards = ["Andrewmap1.txt", "Andrewmap2.txt", "Andrewmaplarge1.txt", "Andrewmaplarge2.txt", "Andrewmaplarge3.txt"]
    
    for bname in boards:
        venue = bname.split('.')[0]
        print "Processing", bname
        with open(os.path.join("results", venue+".txt"), 'w') as f:
            with stdout_redirected(f):
                board = boardFromFile(bname)
                print "Playing on", bname
                print >> sys.stderr, "Playing on", bname
                print "\n".join([" ".join([str(num) for num in row]) for row in board])
                print >> sys.stderr, "\n".join([" ".join([str(num) for num in row]) for row in board])
                
                print '='*80
                print >> sys.stderr, '='*80
                print "Minimax vs. Minimax"
                print >> sys.stderr, "Minimax vs. Minimax"
                playGame(False, False, minimaxDepth=3)

                print '-'*80
                print >> sys.stderr, '-'*80
                print "Alphabeta vs. Alphabeta"
                print >> sys.stderr, "Alphabeta vs. Alphabeta"
                playGame(True, True, alphabetaDepth=4)

                print '-'*80
                print >> sys.stderr, '-'*80
                print "Minimax vs. Alphabeta"
                print >> sys.stderr, "Minimax vs. Alphabeta"
                playGame(False, True, 3, 4)

                print '-'*80
                print >> sys.stderr, '-'*80
                print "Alphabeta vs. Minimax"
                print >> sys.stderr, "Alphabeta vs. Minimax"
                playGame(True, False, 3, 4)
        print "Done processing", bname
