from Queue import PriorityQueue

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
                print self.debug(path) # debug
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
                print self.debug(path) # debug
                return path
            else: # recursive case
                for adj, direction in self.adjacent(coord):
                    if adj not in visited:
                        stack.append((adj, path + direction))
        return [] # impossible

    def greedy(self):

    return []

    def greedy_manhattan_distance(self, goalPos, currPos):
    #heuristic function
    #distance = 0  
    distance = abs(goalPos[0] - currPos[0]) + abs(goalPos[1] - currPos[1])
    return distance

    def debug(self, path):
        # debug with given path
        visited = set()
        currCoord = self.currPos
        visited.add(currCoord)
        for direction in path:
            currRow, currCol = currCoord
            if direction == 'E':
                currCoord = (currRow, currCol+1)
            elif direction == 'S':
                currCoord = (currRow+1, currCol)
            elif direction == 'W':
                currCoord = (currRow, currCol-1)
            elif direction == 'N':
                currCoord = (currRow-1, currCol)
            else:
                print "WARNING: something wrong with debug"
            visited.add(currCoord)
        return "\n".join(["".join(['V' if (row, col) in visited else char for col, char in enumerate(line)]) for row, line in enumerate(self.maze)])
    
    def __str__(self):
        """To string method."""
        return "\n".join(["".join(line) for line in self.maze])

with open("mediumMaze.txt", 'r') as f:
    m = Maze(f)
