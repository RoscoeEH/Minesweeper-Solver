from minesweeperLogic import Board

# Returns a list if coords for surrounding squares
def surroundingCoords(info, x, y):
    pass


# Holds the solvers info on the board
class Info:
    def __init__(self, board):
        self.width = board.width
        self.height = board.height
        self.markedMap = board.getState() # Marked mines are -2 unknown is -1
        self.minesLeft = board.numMines


# If all bombs are marked update all unmarked unknowne squares
def checkRemaining(info, toCheck):
    if info.minesLeft[0] == 0:
        for y, row in enumerate(info.markedMap):
            for x, item in enumerate(row):
                if item == -1:
                    toCheck.append([x,y])

# Marks all obvious bombs and checks all obvious squares
def easyGets(info, toCheck):
    for y, row in enumerate(info.markedMaps):
        for x, item in enumerate(row):
            # If the item isn't unknown or marked check its surroundings
            # All squares around 0s are already cleared by update
            if item > 0:
                surroundingFlags = 0
                remainingSquares = 0
            ### Currently working on ###


# Checks for less obvious bombs by solving a system of linear equations based on the board
def nothingObvious(info, toCheck):
    pass

# Checks squares on the board and updates info accordingly
def update(board, info, toCheck):
    for square in toCheck:
        for newSquare in board.checkSquare([square]):
            # newSquare contains an [x,y] that have a new number to be added to info
            info.markedMap[newSquare[1]][newSquare[0]] = board.map[newSquare[1]][newSquare[0]]



# Function that takes an instance of board and plays minesweeper on it
def play(board):
    # Start the game in the middle of the board
    board.start(board.width // 2, board.height // 2)

    # This functions board copy
    # Will update with each check
    # Marked squares labeled -2
    info = Info(board)


    # Main loop will stop when game is won or lost
    while board.knownCount > 0 and not board.gameLost:
        
        # Array of squares that have been determined to be clear
        toCheck = []
        # Keeps number of mines left at the start of a round to see if a fuction has marked any bombs
        flagsRemaining = info.minesLeft

        # Checks are done in order of speed of computation

        # First check if by far the fastest and wins the game if it is used
        checkRemaining(info, toCheck)
        
        if toCheck != []:
            update(board, info, toCheck)
            # All bombs should be known here so braak to loop
            break

        # This will be the most commonly used section of the checks.
        easyGets(info, toCheck)

        # If this is used it should skip to the next check to avoid using nothingObvious() whenever possible
        if toCheck != []:
            update(board, info, toCheck)
            continue
        
        # This means nothing has been cleared or flagged this pass
        if flagsRemaining == info.minesLeft:
            nothingObvious(info, toCheck)

            # If nothing has been found nothing will be found in the future so raise an execption
            # A final implementation of nothingObvious() will include a probabalistic guess if nothing can be completely determined
            if toCheck == [] and flagsRemaining == info.minesLeft:
                raise Exception("No move selected")
            
            # last update before restarting the loop
            update(board, info, toCheck)

    
    # Checks if the solver won or lost
    if board.knownCount == 0:
        return True
    if board.gameLost:
        return False
    
    # Something is wrong
    raise Exception("Unknown end condition")