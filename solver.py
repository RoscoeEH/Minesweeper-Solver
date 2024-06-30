from minesweeperLogic import Board

# Returns a list if coords for surrounding squares
def getSurrounding(info, x, y):
    # All surrounding coords for a center square
    surrounding = []
    for ny in range(y-1, y+2):
        for nx in range(x-1, x+2):
            # Skip the target
            if nx == x and ny == y:
                continue
            if 0 < nx < info.width and 0 < ny < info.height:
                surrounding.append([nx,ny])
    return surrounding


# Takes a list of coords and returns the number of surrounding bombs and unknown squares
def countSurrounding(info, surrounding):
    bombs = 0
    unknown = 0
    for square in surrounding:
        if info.markedMap[square[1]][square[0]] == -2:
            bombs += 1
        elif info.markedMap[square[1]][square[0]] == -1:
            unknown += 1
    return bombs, unknown


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
            if item <= 0:
                continue

            surrounding = getSurrounding(info, x, y)
            # Count marked bombs and unknown squares
            bombs, unknown = countSurrounding(info, surrounding)

            # updates marks and adds new bombs too be checked
            # and conditions prevent unneccasary loops
            if bombs == item and len(surrounding) != bombs:
                # add unknown to toCheck
                for square in surrounding:
                    if info.markedMap[square[1]][square[0]] == -1:
                        toCheck.append(square)
            elif unknown == item - bombs and unknown != 0:
                # mark remaining bombs
                for square in surrounding:
                    if info.markedMap[square[1]][square[0]] == -1:
                        info.markedMap[square[1]][square[0]] = -2

# function for elementary operation of swapping two rows
def swap_row(mat, i, j):
 
    for k in range(N + 1):
 
        temp = mat[i][k]
        mat[i][k] = mat[j][k]
        mat[j][k] = temp


# function to reduce matrix to r.e.f.
def rhoReduction(mat):
    for k in range(N):
       
        # Initialize maximum value and index for pivot
        i_max = k
        v_max = mat[i_max][k]
 
        # find greater amplitude for pivot if any
        for i in range(k + 1, N):
            if (abs(mat[i][k]) > v_max):
                v_max = mat[i][k]
                i_max = i
 
        # if a principal diagonal element  is zero,
        # it denotes that matrix is singular, and
        # will lead to a division-by-zero later.
        if not mat[k][i_max]:
            return k    # Matrix is singular
 
        # Swap the greatest value row with current row
        if (i_max != k):
            swap_row(mat, k, i_max)
 
        for i in range(k + 1, N):
 
            # factor f to set current row kth element to 0,
            # and subsequently remaining kth column to 0 */
            f = mat[i][k]/mat[k][k]
 
            # subtract fth multiple of corresponding kth
            # row element*/
            for j in range(k + 1, N + 1):
                mat[i][j] -= mat[k][j]*f
 
            # filling lower triangular matrix with zeros*/
            mat[i][k] = 0
 
        # print(mat);        //for matrix state
 
    # print(mat);            //for matrix state
    return -1



# Checks for less obvious bombs by solving a system of linear equations based on the board
def nothingObvious(info, toCheck):
    pass
    # Build the matrix
    # Pick a square with sorounding bombs and add those
    # Pick a bomb and add its surrounding squares
    # Repeat till the matrix is large enough

    
    

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