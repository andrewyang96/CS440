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
        numNodes = 0
        while len(queue) > 0:
            coord, path = queue.pop(0)
            visited.add(coord)
            if self.getChar(coord) == '%': # wall
                pass
            elif self.getChar(coord) == '.': # goal
                print "Num Nodes:", numNodes
                print self.debug(path) # debug
                return path
            else: # recursive case
                for adj, direction in self.adjacent(coord):
                    if adj not in visited and self.getChar(adj) != '%':
                        numNodes += 1
                        queue.append((adj, path + direction))
        return [] # impossible

    def dfs(self):
        # returns a list of coords that compose path
        # directions: "N", "E", "S", "W"
        # return self._dfs([self.currPos,], [], [])
        stack = [(self.currPos, [], set()),]
        bestPath = None
        numNodes = 0
        while len(stack) > 0:
            coord, path, visited = stack.pop()
            visited = visited.copy()
            visited.add(coord)
            if bestPath is not None and len(path) >= len(bestPath):
                pass
            elif self.getChar(coord) == '%': # wall
                pass
            else: # recursive case
                if self.getChar(coord) == '.': # goal
                    print "Num Nodes:", numNodes
                    print self.debug(path)
                    return path # return on first path found
                    print "Found a path:", path
                    if bestPath is None or len(path) < len(bestPath):
                        print "Is best path"
                        bestPath = path[:]
                for adj, direction in self.adjacent(coord):
                    if adj not in visited and self.getChar(adj) != '%':
                        numNodes += 1
                        stack.append((adj, path + direction, visited))
        print self.debug(bestPath) # debug
        return bestPath

    def greedy(self):
        # like DFS, but puts coords closest to goal up front
        pq = PriorityQueue(maxsize=0)
        pq.put_nowait((self.greedy_manhattan_distance(self.currPos, self.goalPos), (self.currPos, [], set())))
        bestPath = None
        numNodes = 0
        while not pq.empty():
            priority, curr = pq.get_nowait()
            coord, path, visited = curr
            visited = visited.copy()
            visited.add(coord)
            if bestPath is not None and len(path) >= len(bestPath):
                pass
            elif self.getChar(coord) == '%': # wall
                pass
            else: # recursive case
                if self.getChar(coord) == '.': # goal
                    print "Num Nodes:", numNodes
                    print self.debug(path)
                    return path # return on first path found
                    print "Found a path:", path
                    if bestPath is None or len(path) < len(bestPath):
                        print "Is best path"
                        bestPath = path[:]
                for adj, direction in self.adjacent(coord):
                    if adj not in visited and self.getChar(adj) != '%':
                        numNodes += 1
                        heur = self.greedy_manhattan_distance(adj, self.goalPos)
                        if bestPath is None or heur < bestHeur: # preselect based on heuristic
                            pq.put_nowait((heur, (adj, path + direction, visited)))
        print self.debug(bestPath) # debug
        return bestPath

    def a_star(self):
        # like BFS, but puts coords with lowest heuristic (path length + manhattan dist to goal) up front
        pq = PriorityQueue(maxsize=0)
        pq.put_nowait((self.greedy_manhattan_distance(self.currPos, self.goalPos), (self.currPos, [], set())))
        bestPath = None
        bestHeur = None
        numNodes = 0
        while not pq.empty():
            priority, curr = pq.get_nowait()
            coord, path, visited = curr
            visited = visited.copy()
            visited.add(coord)
            if bestPath is not None and priority >= bestHeur:
                pass
            elif self.getChar(coord) == '%': # wall
                pass
            else: # recursive case
                if self.getChar(coord) == '.': # goal
                    print "Found a path:", path
                    if bestPath is None or len(path) < len(bestPath):
                        print "Is best path"
                        bestPath = path[:]
                        bestHeur = priority
                for adj, direction in self.adjacent(coord):
                    if adj not in visited and self.getChar(adj) != '%':
                        numNodes += 1
                        heur = len(path + direction) + self.greedy_manhattan_distance(adj, self.goalPos)
                        if bestPath is None or heur < bestHeur: # preselect based on heuristic
                            pq.put_nowait((heur, (adj, path + direction, visited)))
        print "Num Nodes:", numNodes
        print self.debug(bestPath) # debug
        return bestPath

    def a_star_penalize(self, forwardPenalty, turnPenalty):
        # part 1.2
        # using euclidean heuristic (not manhattan)
        pq = PriorityQueue(maxsize=0)
        pq.put_nowait((self.euclidean_heuristic(self.currPos, self.goalPos), (self.currPos, [], set())))
        bestPath = None
        bestHeur = None
        numNodes = 0
        while not pq.empty():
            priority, curr = pq.get_nowait()
            coord, path, visited = curr
            visited = visited.copy()
            visited.add(coord)
            if bestPath is not None and priority >= bestHeur:
                pass
            elif self.getChar(coord) == '%': # wall
                pass
            else: # recursive case
                if self.getChar(coord) == '.': # goal
                    print "Found a path:", path
                    if bestPath is None or len(path) < len(bestPath):
                        bestPath = path[:]
                for adj, direction in self.adjacent(coord):
                    if adj not in visited and self.getChar(adj) != '%':
                        numNodes += 1
                        heur = self.calculate_penalty(path + direction, forwardPenalty, turnPenalty) + self.euclidean_heuristic(adj, self.goalPos)
                        if bestPath is None or heur < bestHeur: # preselect based on heuristic
                            pq.put_nowait((heur, (adj, path + direction, visited)))
        print "Num Nodes:", numNodes
        print self.debug(bestPath) # debug
        return bestPath

    def greedy_manhattan_distance(self, currPos, goalPos):
        return abs(currPos[0] - goalPos[0]) + abs(currPos[1] - goalPos[1])

    def euclidean_heuristic(self, currPos, goalPos):
        return (currPos[0] - goalPos[0])**2 + (currPos[1] - goalPos[1])**2

    def calculate_penalty(self, path, forwardPenalty, turnPenalty):
        # helper function for a_star_penalize
        if len(path) <= 1:
            return len(path) * forwardPenalty

        accum = 0
        for idx, direction in enumerate(path):
            if idx > 0:
                if path[idx] == path[idx-1]: # forward
                    accum += forwardPenalty
                else: # turn
                    accum += turnPenalty
            else:
                accum += forwardPenalty
        return accum

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

def printMazeCasesPart11(f, name, runDFS=True, runBFS=True, runGreedy=True, runAStar=True):
    print name
    print '-'*80
    
    m = Maze(f)

    if runDFS:
        print "DFS"
        dfs = m.dfs()
        print "Path:", dfs
        print

    if runBFS:
        print "BFS"
        bfs = m.bfs()
        print "Path:", bfs
        print

    if runGreedy:
        print "Greedy Best-First Search"
        gbfs = m.greedy()
        print "Path:", gbfs
        print

    if runAStar:
        print "A*"
        astar = m.a_star()
        print "Path:", astar
        print

def printMazeCasesPart12(f, name):
    print name
    print '-'*80

    m = Maze(f)

    print "Forward: 2, Turn: 1"
    twoone = m.a_star_penalize(2, 1)
    print "Path:", twoone
    print

    print "Forward: 1, Turn: 2"
    onetwo = m.a_star_penalize(1, 2)
    print "Path:", onetwo
    print

# part 1.1
with open("mediumMaze.txt", 'r') as f:
    printMazeCasesPart11(f, "Medium Maze")
with open("bigMaze.txt", 'r') as f:
    printMazeCasesPart11(f, "Big Maze")
with open("openMaze.txt", 'r') as f:
    printMazeCasesPart11(f, "Open Maze", True, False, False, False)

# part 1.2
with open("smallTurns.txt", 'r') as f:
    printMazeCasesPart12(f, "Small Turns")
with open("bigTurns.txt", 'r') as f:
    printMazeCasesPart12(f, "Big Turns")
