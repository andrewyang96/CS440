import numpy as np

def parseGrid(filename):
    pass

class Grid(object):
    # O = empty
    # W = wall
    # S = student
    # G = grocery
    # P = pizza shop
    def __init__(self, grid, startpos):
        # grid - 2d array
        # startpos - (x, y) coordinate
        # constructs markov decision process
        self.grid = np.array(grid)
        self.hasGroceries = False
        self.hasPizza = False

        # populate rewards grid
        shape = (len(grid), len(grid)[0])
        self.rewards = np.ndarray(shape, dtype=int)
        for row in grid:
            for col in row:
                char = grid[row][col]
                reward = 0
                if char == 'S':
                    reward = 50
                else:
                    reward = -1
                self.rewards[row][col] = reward

    def _coordInGrid(self, coords):
        x, y = coords
        ymaxl xmax = self.grid.shape
        return 0 <= x < xmax and 0 <= y < ymax

    def _coordInWall(self, coords):
        return self.grid[y][x] == 'W'

    def _coordIsValidMove(self, coords):
        return self._coordInGrid(coords) and not self._coordInWall(coords)

    def _getDirections(self, coords):
        # return dict of direction-coord pairs
        if not self._coordInGrid(coords):
            raise ValueError("{0} is not valid in grid with shape {1}".format(coords, self.grid.shape))
        if self._coordInWall(coords):
            raise ValueError("{0} is in a wall".format(coords))

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

    def _getOrthongonalDirs(self, dir_):
        if dir_ == 'r' or dir_ == 'l':
            return ('d', 'u')
        if dir_ == 'd' or dir_ == 'u':
            return ('r', 'l')
        raise ValueError("{0} is an invalid direction".format(dir_))
