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

    def bfs(self):

        return self._bfs([self.currPos,], []. [])

    def _bfs(self, queue, visited, path):
         # recursive helper method for dfs
        # stack and visited is list of coords (row, col)
        # path is list of coords
        visited.enqueu(queue[0]) # add coord to visited FIRST
        coord = queue[0]
        currRow, currCol = queue[0]
        if len(queue) == 0: # base case
            print "queue is empty"
            return path + self._dfs(queue, visited, path)
        queue.dequeue(0) # pop from queue AFTER EMPTY queue CHECK
        if self.getChar(coord) == '%': # wall
            print coord, "is wall"
            return path + self._dfs(queue, visited, path)
        elif self.getChar(coord) == '.': # goal
            print coord, "IS GOAL!"
            return path # return path: you're done!
        path.append(coord) # add coord to path AFTER ALL CHECKS
        
        # recursive case: visit each neighbor
        if (currRow, currCol+1) not in visited:
            queue.enqueue((currRow, currCol+1)) # go East
        if (currRow+1, currCol) not in visited:
            queue.enqueue((currRow+1, currCol)) # go South
        if (currRow, currCol-1) not in visited:
            queue.enqueue((currRow, currCol-1)) # go West
        if (currRow-1, currCol) not in visited:
            queue.enqueue((currRow-1, currCol)) # go North
        print "recurse from", currRow, currCol
        return path + self._dfs(queue, visited, path)


    def dfs(self):
        # returns a list of directions to reach goals
        # directions: "N", "E", "S", "W"
        return self._dfs([self.currPos,], [], [])

    def _dfs(self, stack, visited, path):
        # recursive helper method for dfs
        # stack and visited is list of coords (row, col)
        # path is list of coords
        visited.append(stack[0]) # add coord to visited FIRST
        coord = stack[0]
        currRow, currCol = stack[0]
        if len(stack) == 0: # base case
            print "stack is empty"
            return path + self._dfs(stack, visited, path)
        stack.pop(0) # pop from stack AFTER EMPTY STACK CHECK
        if self.getChar(coord) == '%': # wall
            print coord, "is wall"
            return path + self._dfs(stack, visited, path)
        elif self.getChar(coord) == '.': # goal
            print coord, "IS GOAL!"
            return path # return path: you're done!
        path.append(coord) # add coord to path AFTER ALL CHECKS
        
        # recursive case: visit each neighbor
        if (currRow, currCol+1) not in visited:
            stack.append((currRow, currCol+1)) # go East
        if (currRow+1, currCol) not in visited:
            stack.append((currRow+1, currCol)) # go South
        if (currRow, currCol-1) not in visited:
            stack.append((currRow, currCol-1)) # go West
        if (currRow-1, currCol) not in visited:
            stack.append((currRow-1, currCol)) # go North
        print "recurse from", currRow, currCol
        return path + self._dfs(stack, visited, path)
    
    def __str__(self):
        """To string method."""
        return "\n".join(["".join(line) for line in self.maze])

with open("mediumMaze.txt", 'r') as f:
    m = Maze(f)
