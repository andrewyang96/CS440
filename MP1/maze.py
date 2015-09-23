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
            (currRow, currCol+1),
            (currRow+1, currCol),
            (currRow, currCol-1),
            (currRow-1, currCol)
        ]

    def dfs(self):
        # returns a list of coords that compose path
        # directions: "N", "E", "S", "W"
        return self._dfs([self.currPos,], [], [])

    def _dfs(self, stack, visited, path):
        # recursive helper method for dfs
        # stack and visited is list of coords (row, col)
        # path is list of coords
        if len(stack) == 0: # base case
            print "stack is empty"
            return []
        visited.append(stack[0]) # add coord to visited FIRST
        coord = stack.pop(0) # pop from stack AFTER EMPTY STACK CHECK
        print "calling w", coord
        if self.getChar(coord) == '%': # wall
            print coord, "is wall"
            return path + self._dfs(stack, visited, path)
        elif self.getChar(coord) == '.': # goal
            print coord, "IS GOAL!"
            stack[:] = []
            return [] # return path: you're done!
        path.append(coord) # add coord to path AFTER ALL CHECKS
        
        # recursive case: visit each neighbor
        for adj in self.adjacent(coord):
            if adj not in visited:
                stack.append(adj)
        return path + self._dfs(stack, visited, path)
    
    def __str__(self):
        """To string method."""
        return "\n".join(["".join(line) for line in self.maze])

with open("mediumMaze.txt", 'r') as f:
    m = Maze(f)
