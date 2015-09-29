from Queue import PriorityQueue
import os
from PIL import Image, ImageDraw

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
        self.numGhostSpaces = 0 # use in GhostMaze
        for row, line in enumerate(fp):
            line = line.strip() # get rid of newline
            ln = []
            for col, char in enumerate(line):
                ln.append(char)
                if char == 'P':
                    self.currPos = (row, col)
                elif char == '.':
                    self.goalPos = (row, col)
                elif char == 'G':
                    self.initGhostPos = (row, col) # use in GhostMaze
                elif char == 'g':
                    self.numGhostSpaces += 1 # use in GhostMaze
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
        # maxPathLen = 0 # debug
        while len(queue) > 0:
            coord, path = queue.pop(0)
            visited.add(coord)
            #if len(path) > maxPathLen: # debug
            #    maxPathLen = len(path)
            #    print "New max path length", maxPathLen
            
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
                for adj, direction in self.adjacent(coord):
                    if adj not in visited and self.getChar(adj) != '%':
                        numNodes += 1
                        stack.append((adj, path + direction, visited))
        return [] # impossible

    def greedy(self):
        # like DFS, but puts coords closest to goal up front
        pq = PriorityQueue(maxsize=0)
        pq.put_nowait((self.manhattan_distance(self.currPos, self.goalPos), (self.currPos, [])))
        visited = set()
        bestPath = None
        numNodes = 0
        while not pq.empty():
            priority, curr = pq.get_nowait()
            coord, path = curr
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
                for adj, direction in self.adjacent(coord):
                    if adj not in visited and self.getChar(adj) != '%':
                        numNodes += 1
                        heur = self.manhattan_distance(adj, self.goalPos)
                        if bestPath is None: # preselect based on heuristic
                            pq.put_nowait((heur, (adj, path + direction)))
        return [] # impossible

    def a_star(self):
        # like BFS, but puts coords with lowest heuristic (path length + manhattan dist to goal) up front
        pq = PriorityQueue(maxsize=0)
        pq.put_nowait((self.manhattan_distance(self.currPos, self.goalPos), (self.currPos, [])))
        visited = set()
        bestPath = None
        bestHeur = None
        numNodes = 0
        while not pq.empty():
            priority, curr = pq.get_nowait()
            coord, path = curr
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
                        heur = len(path + direction) + self.manhattan_distance(adj, self.goalPos)
                        if bestPath is None or heur < bestHeur: # preselect based on heuristic
                            pq.put_nowait((heur, (adj, path + direction)))
        print "Num Nodes:", numNodes
        print self.debug(bestPath) # debug
        return bestPath

    def a_star_penalize(self, forwardPenalty, turnPenalty):
        # part 1.2
        # using euclidean heuristic (not manhattan)
        pq = PriorityQueue(maxsize=0)
        pq.put_nowait((self.manhattan_distance(self.currPos, self.goalPos), (self.currPos, [])))
        visited = set()
        bestPath = None
        bestHeur = None
        numNodes = 0
        while not pq.empty():
            priority, curr = pq.get_nowait()
            coord, path = curr
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
                        heur = self.calculate_penalty(path + direction, forwardPenalty, turnPenalty) + self.manhattan_distance(adj, self.goalPos) * forwardPenalty
                        if bestPath is None or heur < bestHeur: # preselect based on heuristic
                            pq.put_nowait((heur, (adj, path + direction)))
        print "Num Nodes:", numNodes
        print self.debug(bestPath) # debug
        return bestPath

    def manhattan_distance(self, currPos, goalPos):
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
        if path is None:
            return "None!"
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
        return "\n".join(["".join(['.' if (row, col) in visited and char != 'P' else char for col, char in enumerate(line)]) for row, line in enumerate(self.maze)])
    
    def __str__(self):
        """To string method."""
        return "\n".join(["".join(line) for line in self.maze])

class GhostMaze(Maze):
    # part 1.3
    def __init__(self, fp):
        Maze.__init__(self, fp)
        # calculate ghost trajectory
        self.ghostPosList = []
        currGhostPos = self.initGhostPos
        direction = 1 # face right at first
        for i in xrange(self.numGhostSpaces*2):
            self.ghostPosList.append(currGhostPos)
            nextGhostPos = (currGhostPos[0], currGhostPos[1] + direction)
            if self.getChar(nextGhostPos) == '%': # reverse dir
                direction *= -1
                nextGhostPos = (currGhostPos[0], currGhostPos[1] + direction)
            currGhostPos = nextGhostPos

    def getGhostPos(self, path):
        # get curr ghost position based on length of path
        return self.ghostPosList[len(path) % (self.numGhostSpaces*2)]

    def a_star_ghost(self):
        pq = PriorityQueue(maxsize=0)
        pq.put_nowait((self.manhattan_distance(self.currPos, self.goalPos), (self.currPos, [])))
        visited = set()
        bestPath = None
        bestHeur = None
        numNodes = 0
        backwardsPenalty = len(self.maze) * len(self.maze[0]) / 2 # backwards penalty to allow loitering
        while not pq.empty():
            priority, curr = pq.get_nowait()
            coord, path = curr
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
                    if self.getChar(adj) != '%':
                        numNodes += 1
                        heur = len(path + direction) + self.manhattan_distance(adj, self.goalPos)
                        if adj in visited:
                            heur += backwardsPenalty
                        if bestPath is None or heur < bestHeur: # preselect based on heuristic
                            if adj != self.getGhostPos(path + direction) and (adj != self.getGhostPos(path) and coord != self.getGhostPos(path + direction)):
                                # check that next step won't put pacman on same square as ghost, or won't cross paths with ghost
                                pq.put_nowait((heur, (adj, path + direction)))
        print "Num Nodes:", numNodes
        print self.debug(bestPath) # debug
        return bestPath

    def createAnimation(self, dirname, path):
        curdir = os.path.dirname(os.path.realpath(__file__))
        targetdir = os.path.join(curdir, dirname)
        if not os.path.exists(targetdir):
            os.mkdir(targetdir)
        print "Found target directory"
        # now create frames
        fnameLen = len(path) / 10 + 1
        dim = (len(self.maze[0]), len(self.maze))
        currCoord = self.currPos
        visited = set()
        for i, direction in enumerate(path):
            print "Making frame for index", i
            # get ghost pos
            currGhostPos = self.ghostPosList[i % (self.numGhostSpaces*2)]
            # setup filename
            frame = drawFrame(dim, currCoord, self.maze, visited, currGhostPos)
            fname = os.path.join(targetdir, str(i).zfill(fnameLen) + ".png")
            frame.save(fname, "PNG")
            visited.add(currCoord)
            # move pacman
            if direction == 'E':
                currCoord = (currCoord[0], currCoord[1]+1)
            elif direction == 'S':
                currCoord = (currCoord[0]+1, currCoord[1])
            elif direction == 'W':
                currCoord = (currCoord[0], currCoord[1]-1)
            elif direction == 'N':
                currCoord = (currCoord[0]-1, currCoord[1])
            else:
                raise Exception("Direction not valid: " + direction)
        # final frame
        currGhostPos = self.ghostPosList[len(path) % (self.numGhostSpaces*2)]
        frame = drawFrame(dim, currCoord, self.maze, visited, currGhostPos)
        fname = os.path.join(targetdir, str(i+1).zfill(fnameLen) + ".png")
        frame.save(fname, "PNG")
        print "Done!"
        
def drawFrame(dim, currCoord, mazeArr, visited, ghostPos):
    # walls are black (0,0,0), pacman is yellow (255,255,0), ghost is red (255,0,0), goal is green (0,255,0)
    # background is gray (128,128,128), visited tiles are light gray (192,192,192)
    # each tile is 16x16
    img = Image.new("RGB", (dim[0]*16,dim[1]*16), "black")
    for i, row in enumerate(mazeArr):
        for j, col in enumerate(row):
            char = mazeArr[i][j]
            color = ()
            coord = (i, j)
            if coord in visited:
                color = (192, 192, 192) # visited tile
            else:
                color = (128, 128, 128) # open tile
            
            if char == '%': # wall
                color = (0, 0, 0)
            elif char == '.': # goal
                color = (0, 255, 0)
            elif coord == currCoord: # pacman current position
                color = (255, 255, 0)
            elif coord == ghostPos: # ghost current position
                color = (255, 0, 0)
            writeTile(img, coord, color)
    return img

def writeTile(img, coord, color):
    pixels = img.load()
    for i in range(coord[0]*16, (coord[0]+1)*16):
        for j in range(coord[1]*16, (coord[1]+1)*16):
            pixels[j,i] = color

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

    print "Forward: 1, Turn: 0"
    onetwo = m.a_star_penalize(3, 2)
    print "Path:", onetwo
    print

def printMazeCases13(f, name, dirname):
    print name
    print '-'*80

    m = GhostMaze(f) # change classes

    print "Solution"
    soln = m.a_star_ghost()
    print "Path:", soln
    print "Making animations"
    print m.createAnimation(dirname, soln)

# part 1.1
with open("mediumMaze.txt", 'r') as f:
    printMazeCasesPart11(f, "Medium Maze")
with open("bigMaze.txt", 'r') as f:
    printMazeCasesPart11(f, "Big Maze")
with open("openMaze.txt", 'r') as f:
    printMazeCasesPart11(f, "Open Maze", True, False, True, True)

# part 1.2
with open("smallTurns.txt", 'r') as f:
    printMazeCasesPart12(f, "Small Turns")
with open("bigTurns.txt", 'r') as f:
    printMazeCasesPart12(f, "Big Turns")

# part 1.3
with open("smallGhost.txt", 'r') as f:
    printMazeCases13(f, "Small Ghost", "smallGhost")
with open("mediumGhost.txt", 'r') as f:
    printMazeCases13(f, "Medium Ghost", "mediumGhost")
with open("bigGhost.txt", 'r') as f:
    printMazeCases13(f, "Big Ghost", "bigGhost")
