import numpy as np
import operator

def parseGrid(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            row = list(line.strip())
            grid.append(row)
        return grid

class Grid(object):
    # O = empty
    # W = wall
    # S = student
    # G = grocery
    # P = pizza shop
    # IMPORTANT: x-coord is col num, y-coord is row num
    def __init__(self, grid):
        # grid - 2d array
        # startpos - (x, y) coordinate
        # constructs markov decision process
        self.grid = np.array(grid)
        shape = (len(grid), len(grid[0]))
        template = np.ndarray(shape, dtype=int)

        # self.rewards is a 2d array of numpy ndarrays
        # row 0 indicates no groceries, row 1 indicates one grocery
        # col 0 indicates no pizza, row 0 indicates one pizza
        self.rewards = [[None, None], [None, None]]

        # populate rewards grid for no groceries, no pizza
        rewards = template.copy()
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                reward = 0
                if char == 'G':
                    reward = 25
                else:
                    reward = -1
                rewards[r][c] = reward
        self.rewards[0][0] = rewards

        # populate rewards grid for no groceries, one pizza
        # also populates rewards grid for one grocery, one pizza
        rewards = template.copy()
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                reward = 0
                if char == 'S':
                    reward = 50
                else:
                    reward = -1
                rewards[r][c] = reward
        self.rewards[0][1] = rewards
        self.rewards[1][1] = rewards

        # populate rewards grid for one grocery, no pizza
        rewards = template.copy()
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                reward = 0
                if char == 'P':
                    reward = 25
                else:
                    reward = -1
                rewards[r][c] = reward
        self.rewards[1][0] = rewards

        # populate directions (actions) for each state (pos in grid)
        self.dirs = []
        for r, row in enumerate(grid):
            dirRow = []
            for c, char in enumerate(row):
                dir_ = self._getDirections((c, r))
                dirRow.append(dir_)
            self.dirs.append(dirRow)

    def _getReward(self, coords, hasGroceries, hasPizza):
        x, y = coords
        return self.rewards[hasGroceries][hasPizza][y][x]

    def _coordInGrid(self, coords):
        x, y = coords
        ymax, xmax = self.grid.shape
        return 0 <= x < xmax and 0 <= y < ymax

    def _coordInWall(self, coords):
        x, y = coords
        return self.grid[y][x] == 'W'

    def _coordIsValidMove(self, coords):
        return self._coordInGrid(coords) and not self._coordInWall(coords)

    def _getDirections(self, coords):
        # return dict of direction-coord pairs
        if not self._coordInGrid(coords):
            raise ValueError("{0} is not valid in grid with shape {1}".format(coords, self.grid.shape))
        if self._coordInWall(coords):
            # raise ValueError("{0} is in a wall".format(coords))
            return {}

        x, y = coords
        dirs = {}
        right = (x+1, y)
        dirs['r'] = right if self._coordIsValidMove(right) else coords
        down = (x, y+1)
        dirs['d'] = down if self._coordIsValidMove(down) else coords
        left = (x-1, y)
        dirs['l'] = left if self._coordIsValidMove(left) else coords
        up = (x, y-1)
        dirs['u'] = up if self._coordIsValidMove(up) else coords
        return dirs

    def _getOrthogonalDirs(self, dir_):
        if dir_ == 'r' or dir_ == 'l':
            return ('d', 'u')
        if dir_ == 'd' or dir_ == 'u':
            return ('r', 'l')
        raise ValueError("{0} is an invalid direction".format(dir_))

    def _estimateFutureValue(self, dir_, coords, rewardsGrid):
        # 90% probability correct dir, 5% probability each orthogonal dir
        x, y = coords
        correctX, correctY = self.dirs[y][x][dir_]
        correctDirVal = 0.9 * rewardsGrid[correctY][correctX]
        
        orthoDirVals = []
        for orthoDir in self._getOrthogonalDirs(dir_):
            orthoX, orthoY = self.dirs[y][x][orthoDir]
            orthoDirVal = 0.05 * rewardsGrid[orthoY][orthoX]
            orthoDirVals.append(orthoDirVal)

        return correctDirVal + sum(orthoDirVals)

    def _estimateStateActionValue(self, dir_, coords, dirGrid):
        x, y = coords
        correctX, correctY = self.dirs[y][x][dir_]
        correctDirVal = 0.9 * max(dirGrid[correctY][correctX].values())

        orthoDirVals = []
        for orthoDir in self._getOrthogonalDirs(dir_):
            orthoX, orthoY = self.dirs[y][x][orthoDir]
            orthoDirVal = 0.05 * max(dirGrid[correctY][correctX].values())
            orthoDirVals.append(orthoDirVal)

        return correctDirVal + sum(orthoDirVals)

    def _iterateCoord(self, rewardsGrid, dirGrid, learningRate, discountFactor, coords, dir_):
        # s - state (position on grid) <- coords
        # a - action (r, d, l, u) <- dir_
        # Q0(s, a) - old value
        # Q1(s, a) - new value
        # lr - learning rate
        # df - discount factor
        # r - reward for given coords
        # if includeDirs=True, then return tuple: (Q1(s, a), sorted descending array of (value, dir) tuple)
        # Equation:
        # Q1(s, a) = Q0(s, a) + lr * (r + df * max(estimate of future value for each dir in adjacent state) - Q0(s, a))
        # returns dict of direction-value pairs
        x, y = coords
        
        immediateReward = rewardsGrid[y][x] # r
        maxEstFutureVal = self._estimateStateActionValue(dir_, coords, dirGrid) # max(estimate of future value for each dir in adjacent state)
        return dirGrid[y][x][dir_] + learningRate * (immediateReward + discountFactor * maxEstFutureVal - dirGrid[y][x][dir_])

    def _generateInitialDirGrid(self, hasGroceries, hasPizza):
        rewardsGrid = self.rewards[hasGroceries][hasPizza]
        optimalDirGrid = []

        for r, row in enumerate(self.grid):
            optimalDirRow = []
            for c, char in enumerate(row):
                if char == 'W':
                    optimalDirRow.append(None)
                else:
                    rightReward = self._estimateFutureValue('r', (c, r), rewardsGrid)
                    downReward = self._estimateFutureValue('d', (c, r), rewardsGrid)
                    leftReward = self._estimateFutureValue('l', (c, r), rewardsGrid)
                    upReward = self._estimateFutureValue('u', (c, r), rewardsGrid)
                    optimalDirRow.append({'r': rightReward, 'd': downReward, 'l': leftReward, 'u': upReward})
            optimalDirGrid.append(optimalDirRow)
        return optimalDirGrid

    def constructModel(self, hasGroceries, hasPizza, limit=1000, baseLearningRate=60., discountFactor=0.1, debug=False):
        # returns (optimal dir grid, final directions list on the grid)
        # baseLearningRate decays as O(1/t): blr/(blr-1+t)
        rewardsGrid = self.rewards[hasGroceries][hasPizza]
        optimalDirGrid = self._generateInitialDirGrid(hasGroceries, hasPizza)

        for trial in range(1, limit+1):
            learningRate = float(baseLearningRate) / (baseLearningRate - 1 + trial)
            newDirGrid = map(list, optimalDirGrid)
            if debug:
                print "TRIAL", trial
                print
            for r, row in enumerate(self.grid):
                for c, char in enumerate(row):
                    if debug:
                        print "ANALYZING row", r, "col", c
                    if char == 'W':
                        if debug:
                            print "Row", r, "col", c, "is a wall"
                            print
                        newDirGrid[r][c] = None
                    else:
                        if debug:
                            print "Row", r, "col", c, "has value", newGrid[r][c]
                        rightDirVal = self._iterateCoord(rewardsGrid, optimalDirGrid, learningRate, discountFactor, (c, r), 'r')
                        downDirVal = self._iterateCoord(rewardsGrid, optimalDirGrid, learningRate, discountFactor, (c, r), 'd')
                        leftDirVal = self._iterateCoord(rewardsGrid, optimalDirGrid, learningRate, discountFactor, (c, r), 'l')
                        upDirVal = self._iterateCoord(rewardsGrid, optimalDirGrid, learningRate, discountFactor, (c, r), 'u')
                        newDirGrid[r][c] = {'r': rightDirVal, 'd': downDirVal, 'l': leftDirVal, 'u': upDirVal}
                        if debug:
                            print "DIRLIST"
                            dirList = sorted([(rightDirVal, 'r'), (downDirVal, 'd'), (leftDirVal, 'l'), (upDirVal, 'u')], reverse=True)
                            for estVal, dir_ in dirList:
                                print dir_ + ':', estVal
                            print
                                        
            optimalDirGrid = newDirGrid
            if debug:
                print '='*80

        # construct dirListGrid
        bestDirGrid = []
        for r, row in enumerate(optimalDirGrid):
            bestDirRow = []
            for c, dirs in enumerate(row):
                if dirs is None:
                    bestDirRow.append('x')
                else:
                    sortedDirs = sorted(dirs, key=lambda dir_: -dirs[dir_])
                    bestDirRow.append(sortedDirs[0])
            bestDirGrid.append(bestDirRow)
        
        return (optimalDirGrid, bestDirGrid)

class BonusGrid(Grid):
    # H = health, go there after delivering pizza
    def __init__(self, grid):
        super(BonusGrid, self).__init__(grid)

        # populate health rewards grid
        shape = (len(grid), len(grid[0]))
        rewards = np.ndarray(shape, dtype=int)
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                reward = 0
                if char == 'H':
                    reward = 50
                else:
                    reward = -1
                rewards[r][c] = reward
        self.healthRewards = rewards

    def _generateInitalDirGrid(self, hasGroceries, hasPizza, needHealth):
        if needHealth:
            rewardsGrid = self.healthRewards
            optimalDirGrid = []

            for r, row in enumerate(self.grid):
                optimalDirRow = []
                for c, char in enumerate(row):
                    if char == 'W':
                        optimalDirRow.append(None)
                    else:
                        rightReward = self._estimateFutureValue('r', (c, r), rewardsGrid)
                        downReward = self._estimateFutureValue('d', (c, r), rewardsGrid)
                        leftReward = self._estimateFutureValue('l', (c, r), rewardsGrid)
                        upReward = self._estimateFutureValue('u', (c, r), rewardsGrid)
                        optimalDirRow.append({'r': rightReward, 'd': downReward, 'l': leftReward, 'u': upReward})
                optimalDirGrid.append(optimalDirRow)
            return optimalDirGrid
        else:
            return super(BonusGrid, self)._generateInitialDirGrid(hasGroceries, hasPizza)

    def constructModel(self, hasGroceries, hasPizza, needHealth, limit=1000, baseLearningRate=60., discountFactor=0.1, debug=False):
        if needHealth:
            rewardsGrid = self.healthRewards
            optimalDirGrid = self._generateInitialDirGrid(hasGroceries, hasPizza)

            for trial in range(1, limit+1):
                learningRate = baseLearningRate / (baseLearningRate - 1 + trial)
                newDirGrid = map(list, optimalDirGrid)
                if debug:
                    print "TRIAL", trial
                    print
                for r, row in enumerate(self.grid):
                    for c, char in enumerate(row):
                        if debug:
                            print "ANALYZING row", r, "col", c
                        if char == 'W':
                            if debug:
                                print "Row", r, "col", c, "is a wall"
                                print
                            newDirGrid[r][c] = None
                        else:
                            if debug:
                                print "Row", r, "col", c, "has value", newGrid[r][c]
                            rightDirVal = self._iterateCoord(rewardsGrid, optimalDirGrid, learningRate, discountFactor, (c, r), 'r')
                            downDirVal = self._iterateCoord(rewardsGrid, optimalDirGrid, learningRate, discountFactor, (c, r), 'd')
                            leftDirVal = self._iterateCoord(rewardsGrid, optimalDirGrid, learningRate, discountFactor, (c, r), 'l')
                            upDirVal = self._iterateCoord(rewardsGrid, optimalDirGrid, learningRate, discountFactor, (c, r), 'u')
                            newDirGrid[r][c] = {'r': rightDirVal, 'd': downDirVal, 'l': leftDirVal, 'u': upDirVal}
                            if debug:
                                print "DIRLIST"
                                dirList = sorted([(rightDirVal, 'r'), (downDirVal, 'd'), (leftDirVal, 'l'), (upDirVal, 'u')], reverse=True)
                                for estVal, dir_ in dirList:
                                    print dir_ + ':', estVal
                                print
                                            
                optimalDirGrid = newDirGrid
                if debug:
                    print '='*80

            # construct dirListGrid
            bestDirGrid = []
            for r, row in enumerate(optimalDirGrid):
                bestDirRow = []
                for c, dirs in enumerate(row):
                    if dirs is None:
                        bestDirRow.append('x')
                    else:
                        sortedDirs = sorted(dirs, key=lambda dir_: -dirs[dir_])
                        bestDirRow.append(sortedDirs[0])
                bestDirGrid.append(bestDirRow)
            
            return (optimalDirGrid, bestDirGrid)
        else:
            return super(BonusGrid, self).constructModel(hasGroceries, hasPizza, limit, baseLearningRate, discountFactor, debug)

def printBestDirGrid(dirGrid):
    for row in dirGrid:
        print ' '.join([char.upper() for char in row])

def printDirGrid(dirListGrid):
    for r, row in enumerate(dirListGrid):
        for c, dirs in enumerate(row):
            print "Row", r, "col", c, "=", dirs

def testBasic(trials=100, baseLearningRate=60., discountFactor=0.1):
    arr = parseGrid("data/part1_3_data.txt")
    grid = Grid(arr)
    bestDirGrids = [[None, None], [None, None]]
    
    print "The Grid"
    print "Num Trials:", trials
    print "Base Learning Rate:", baseLearningRate
    print "Discount Factor:", discountFactor
    printBestDirGrid(arr)
    print '='*80
    for hasPizza in (False, True):
        for hasGroceries in (False, True):
            print "Has Groceries:", hasGroceries
            print "Has Pizza:", hasPizza
            dirGrid, bestDirGrid = grid.constructModel(hasGroceries, hasPizza, limit=trials, debug=False)
            bestDirGrids[hasGroceries][hasPizza] = bestDirGrid
            # printDirGrid(dirGrid)
            printBestDirGrid(bestDirGrid)
    print

def testDivided(trials=400, baseLearningRate=60., discountFactor=0.1):
    arr = parseGrid("data/part1_3_divided.txt")
    grid = Grid(arr)
    bestDirGrids = [[None, None], [None, None]]
    
    print "The Grid"
    print "Num Trials:", trials
    print "Base Learning Rate:", baseLearningRate
    print "Discount Factor:", discountFactor
    printBestDirGrid(arr)
    print '='*80
    for hasPizza in (False, True):
        for hasGroceries in (False, True):
            print "Has Groceries:", hasGroceries
            print "Has Pizza:", hasPizza
            dirGrid, bestDirGrid = grid.constructModel(hasGroceries, hasPizza, limit=trials, debug=False)
            bestDirGrids[hasGroceries][hasPizza] = bestDirGrid
            # printDirGrid(dirGrid)
            printBestDirGrid(bestDirGrid)
    print

def testBonus(trials=100, baseLearningRate=60., discountFactor=0.1):
    arr = parseGrid("data/part1_3_bonus_data.txt")
    grid = BonusGrid(arr)
    bestDirGrids = [[None, None], [None, None]]
    healthGrid = None
    debug = False

    print "The Grid"
    print "Num Trials:", trials
    print "Base Learning Rate:", baseLearningRate
    print "Discount Factor:", discountFactor
    printBestDirGrid(arr)
    print '='*80
    for hasPizza in (False, True):
        for hasGroceries in (False, True):
            print "Has Groceries:", hasGroceries
            print "Has Pizza:", hasPizza
            dirGrid, bestDirGrid = grid.constructModel(hasGroceries, hasPizza, False, limit=trials, debug=debug)
            bestDirGrids[hasGroceries][hasPizza] = bestDirGrid
            # printDirGrid(dirGrid)
            printBestDirGrid(bestDirGrid)
    
    print "NEED HEALTH"
    dirGrid, bestDirGrid = grid.constructModel(False, False, True, limit=trials, debug=debug)
    healthGrid = bestDirGrid
    # printDirGrid(dirGrid)
    printBestDirGrid(bestDirGrid)
    print

if __name__ == "__main__":
    testBasic()
    testDivided()
    testBonus()
