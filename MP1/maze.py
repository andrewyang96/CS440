class Maze(object):
    """
    % = wall
    P = start
    . = goal
    V = visited
    """
    def __init__(self, fp):
        """Constructor: get maze from file."""
        self.maze = []
        self.currPos = None
        self.goalPos = None
        for row, line in enumerate(fp):
            line = line.strip() # get rid of newline
            ln = []
            for col, char in enumerate(line):
                ln.append(char)
                if char == 'P':
                    self.currPos = (row, col)
                elif char == '.':
                    self.goalPos = (row, col)
            self.maze.append(ln)

    def getChar(self, coord):
        return self.maze[coord[0]][coord[1]]

    def dfs(self):
        # returns a list of directions to reach goals
        # directions: "N", "E", "S", "W"
        return self._dfs(self, [self.currPos,], [])

    def _dfs(self, stack, visited):
        # recursive helper method for dfs
        # stack and visited is list of coords (row, col)
        if len(stack) == 0: # base case
            return []
        elif self.getChar(stack[0]) == '%': # wall
            return []
        # TODO
    
    def __str__(self):
        """To string method."""
        return "\n".join(["".join(line) for line in self.maze])

with open("mediumMaze.txt", 'r') as f:
    m = Maze(f)
