# This File Contains the basic information behind playing minesweeper
# The game state and all ways of manipulating the board the change the game state are here


import random

# Helper function used in assigning numbers to the map
# Take an (x,y) and a map and increment all surrounding values unless the value is -1 (that represents a bomb)
def incrementSurrounding(map, x, y):
    height = len(map)
    width = len(map[0])
    
    # Define the surrounding coordinates relative to (x, y)
    surroundings = [(-1, -1), (-1, 0), (-1, 1),(0, -1),(0, 1),(1, -1), (1, 0), (1, 1)]
    
    # Iterate through each surrounding position
    for dx, dy in surroundings:
        nx, ny = x + dx, y + dy
        # Check if the surrounding position is within bounds
        if 0 <= nx < width and 0 <= ny < height:
            # Does not increment bombs
            if map[ny][nx] != -1:
                map[ny][nx] += 1

# Baseline class of minesweeper
# Contains board all attributes of the current gamestate
class Board:
    def __init__(self, width, height, numMines):
        self.width = width
        self.height = height
        self.numMines = numMines
        # Initializes to all 0s
        # After start, contains all bombs and surrounding bomb values
        self.map = [[0] * width for _ in range(height)]
        # Number of squares that need to be revealed for a win
        self.knownCount = width * height - numMines
        # All squares currently revealed
        self.knownMap = [[0] * width for _ in range(height)] # 1 for known, 0 for unknown
        self.gameLost = False

    # Takes the first squre clicked and the surrounding squares and makes them empty
    # Randomly distributes the mines amoung the remaining squares
    def start(self, startX, startY):
        # This is the number of blank squares
        startBlanks = 9
        if startX == 0 or startX == self.width - 1:
            startBlanks = (startBlanks * 2) // 3
        if startY == 0 or startY == self.height - 1:
            startBlanks = (startBlanks * 2) // 3

        # The number of bombs plus 0s to fill all other squares except those that are forced to be blank by the start value
        bombLocs = [-1] * self.numMines + [0] * (self.width * self.height - self.numMines - startBlanks)

        # Place the bombs randomly
        random.shuffle(bombLocs)
        

        # Finds the value in the flat list cooresponding to (startX, startY)
        target = startX + startY * self.width
        
        ### The following block goes through the flat list and inserts 0s at the start square and all surrounding squares ###
        ### This must be done in order otherwise bombs can be shifted into the starting squares                           ###

        # Check above the target value
        if startY > 0:
            # Check diagonally above-left
            if startX > 0:
                bombLocs.insert(target - self.width - 1, 0)
            # Inserts directly above
            bombLocs.insert(target - self.width, 0)
            # Check diagonally above-right
            if startX < self.width - 1:
                bombLocs.insert(target - self.width + 1, 0)
        # Check left
        if startX > 0:
            bombLocs.insert(target - 1, 0)
        # Inserts target
        bombLocs.insert(target, 0)
        # Check right
        if startX < self.width - 1:
            bombLocs.insert(target + 1, 0)
        # Check below
        if startY < self.height - 1:
            # Check diagonally below-left
            if startX > 0:
                bombLocs.insert(target + self.width - 1, 0)
            # Inserts Below
            bombLocs.insert(target + self.width, 0)
            # Check diagonally below-right
            if startX < self.width - 1:
                bombLocs.insert(target + self.width + 1, 0)


        # Goes through and adds the bombs to self.map
        # Increments values that represent surrounding bombs
        for i, item in enumerate(bombLocs):
            x = i % self.width
            y = i // self.width
            
            if item == -1:
                self.map[y][x] = -1
                
                incrementSurrounding(self.map, x, y)

    # Reset board to default state
    def reset(self):
        self.map = [[0] * self.width for _ in range(self.height)]
        self.knownCount = self.width * self.height - self.numMines
        self.knownMap = [[0] * self.width for _ in range(self.height)]
        self.gameLost = False


    # This takes a squares coordinates and and returns the list of squares to be cleared
    # If it finds a 0 square it recursivly clears all surrounding squares
    def _checkSquare(self, toCheck):
        x = toCheck[-1][0]
        y = toCheck[-1][1]

        # Clear surrounding
        if self.map[y][x] == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if [nx,ny] in toCheck:
                        continue  # Skip the current square itself
                    if 0 <= nx < self.width and 0 <= ny < self.height and (nx,ny) not in toCheck:
                        toCheck += [[nx,ny]]
                        self._checkSquare(toCheck)
        return toCheck

    # The wrapper function for _checkSquare()
    # This makes it easier to do other checks after the squares have all been returned
    def checkSquare(self, toCheck):
        result = self._checkSquare(toCheck)

        # Loss condition
        if self.map[result[0][1]][result[0][0]] == -1:
            self.gameLost = True
        else:
            # Updates known count to see how many are left to remove
            for square in result:
                # Makes sure not to count cleared squares twice
                if self.knownMap[square[1]][square[0]] != 1:
                    self.knownCount -= 1
                    self.knownMap[square[1]][square[0]] = 1
        return result

    # Returns an array where -1 represents unknown to the player and if known has the number
    def getState(self):
        known = []

        for row in range(self.height):
            currentRow = []
            for col in range(self.width):
                if self.knownMap[row][col] == 1:
                    currentRow.append(self.map[row][col])
                else:
                    currentRow.append(-1)
            known.append(currentRow)
        
        return known