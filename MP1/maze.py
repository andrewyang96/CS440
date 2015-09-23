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
        # helper method
        return self.maze[coord[0]][coord[1]]

    def adjacent(self, coord):
        # helper method
        currRow, currCol = coord
        return [
            ((currRow, currCol+1), ['E',]),
            ((currRow+1, currCol), ['S',]),
            ((currRow, currCol-1), ['W',]),
            ((currRow-1, currCol), ['N',])
        ]
    
    def bfs(self):
        queue = [(self.currPos, []),]
        visited = set()
        while len(queue) > 0:
            coord, path = queue.pop(0)
            visited.add(coord)
            if self.getChar(coord) == '%': # wall
                pass
            elif self.getChar(coord) == '.': # goal
                return path
            else: # recursive case
                for adj, direction in self.adjacent(coord):
                    if adj not in visited:
                        queue.append((adj, path + direction))
        return [] # impossible

    def dfs(self):
        # returns a list of coords that compose path
        # directions: "N", "E", "S", "W"
        # return self._dfs([self.currPos,], [], [])
        stack = [(self.currPos, []),]
        visited = set()
        while len(stack) > 0:
            coord, path = stack.pop()
            visited.add(coord)
            if self.getChar(coord) == '%': # wall
                pass
            elif self.getChar(coord) == '.': # goal
                return path
            else: # recursive case
                for adj, direction in self.adjacent(coord):
                    if adj not in visited:
                        stack.append((adj, path + direction))
        return [] # impossible
    
    def __str__(self):
        """To string method."""
        return "\n".join(["".join(line) for line in self.maze])

with open("mediumMaze.txt", 'r') as f:
    m = Maze(f)
