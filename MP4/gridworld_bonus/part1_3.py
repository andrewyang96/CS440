import numpy as np

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
    def __init__(self, grid, startpos):
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

    def _iterateCoord(self, rewardsGrid, learningRate, discountFactor, coords, includeDirs=False):
        # s - state (position on grid)
        # a - action (r, d, l, u)
        # Q0(s, a) - old value
        # Q1(s, a) - new value (return value given includeDirs=False)
        # lr - learning rate
        # df - discount factor
        # r - reward for given coords
        # if includeDirs=True, then return tuple: (Q1(s, a), sorted descending array of (value, dir) tuple)
        # Equation:
        # Q1(s, a) = Q0(s, a) + lr * (r + df * max(estimate of future value for each dir) - Q0(s, a))
        x, y = coords
        oldVal = rewardsGrid[y][x]

        rightVal = self._estimateFutureValue('r', coords, rewardsGrid)
        downVal = self._estimateFutureValue('d', coords, rewardsGrid)
        leftVal = self._estimateFutureValue('l', coords, rewardsGrid)
        upVal = self._estimateFutureValue('u', coords, rewardsGrid)

        optimalVal = max(rightVal, downVal, leftVal, upVal)
        if includeDirs:
            return (optimalVal, sorted([(rightVal, 'r'), (downVal, 'd'), (leftVal, 'l'), (upVal, 'u')], reverse=True))
        else:
            return optimalVal

    def constructModel(self, hasGroceries, hasPizza, limit=1000, debug=False):
        # returns (final rewards grid, optimal dir grid, final directions list on the grid)
        baseLearningRate = 60. # decays as O(1/t): blr/(blr-1+t)
        discountFactor = 0.1
        currGrid = self.rewards[hasGroceries][hasPizza].copy()
        optimalDirGrid = []
        dirListGrid = []

        for trial in range(1, limit+1):
            learningRate = baseLearningRate / (baseLearningRate - 1 + trial)
            newGrid = map(list, currGrid) # deepcopy
            if debug:
                print "TRIAL", trial
                print
            for r, row in enumerate(self.grid):
                optimalDirRow = []
                dirListRow = []
                
                for c, char in enumerate(row):
                    if debug:
                        print "ANALYZING row", r, "col", c
                    if char == 'W':
                        newGrid[r][c] = currGrid[r][c]
                        if debug:
                            print "Row", r, "col", c, "is a wall"
                            print
                        if trial == limit:
                            # expect contribution to optimalDirRow
                            optimalDirRow.append('x')
                    else:
                        if debug:
                            print "Row", r, "col", c, "has value", newGrid[r][c]
                        if trial == limit:
                            # last trial: expect contribution to optimalDirRow
                            newGrid[r][c], dirList = self._iterateCoord(currGrid, learningRate, discountFactor, (c, r), includeDirs=True)
                            optimalDirRow.append(dirList[0][1])
                            dirListRow.append(dirList)
                            if debug:
                                print "DIRLIST"
                                for value, dir_ in dirList:
                                    print dir_ + ':', value
                        else:
                            newGrid[r][c] = self._iterateCoord(currGrid, learningRate, discountFactor, (c, r))
                            if debug:
                                print
                
                if len(optimalDirRow) > 0:
                    optimalDirGrid.append(optimalDirRow)
                if len(dirListRow) > 0:
                    dirListGrid.append(dirListRow)
            
            currGrid = newGrid
            if debug:
                print '='*80
        return (currGrid, optimalDirGrid, dirListGrid)

def printDirGrid(dirGrid):
    for row in dirGrid:
        print ' '.join([char.upper() for char in row])

def printDirListGrid(dirListGrid):
    for r, row in enumerate(dirListGrid):
        for c, dirs in enumerate(row):
            print "Row", r, "col", c, "=", dirs

if __name__ == "__main__":
    arr = parseGrid("data/part1_3_data.txt")
    grid = Grid(arr, (2,6))
    dirListGrids = [[None, None], [None, None]]
    
    print "The Grid"
    printDirGrid(arr)
    print '='*80
    for hasPizza in (False, True):
        for hasGroceries in (False, True):
            print "Has Groceries:", hasGroceries
            print "Has Pizza:", hasPizza
            finalRewardsGrid, optimalDirGrid, dirListGrid = grid.constructModel(hasGroceries, hasPizza, limit=20, debug=False)
            dirListGrids[hasGroceries][hasPizza] = dirListGrid
            printDirGrid(optimalDirGrid)
            printDirListGrid(dirListGrid)
