# Minesweeper-Solver
A playable minesweeper game written in python that impliments a linear algebra based solver.
The classic game Minesweeper consists of a grid where a set of random squares have been labelled as bombs. The remaining squares contain a number representing the number of bombs that are surrounding that square. The player then goes about marking the squares they suspect to contain bombs and revealing the others. The game is won when all non-bomb squares are revealled, it is lost if a bomb is found.
## Backround Logic
The file minesweeperLogic.py contains the background game state. It makes alterations to the board based on player inputs and keeps this updates in a class.
### Existing Elements
#### Board()
The board class contains all neccesary elements of the game state. It is initialized with the width and height of the board, along with the number of mines to place on the map. It then generates "map" an array of all bombs (represented as -1) and the numbers coorsponding to each square. These values are initialized to 0 for reasons to be explained in the description of the "start" sub-routine. It also holds an array of what squares have been revealed to the player, a count on the number of squares to be revealed for a win, and a boolean stating whether a bomb has been revealed.
##### Board.start(x,y):
For the convience of the player, it is helpful to make sure that the first square revealed is not a bomb. If it where the game would be over essentially on a coin flip with no information. To prevent the need for further early guessing it helps to make sure that all the squares surrounding the start square are also not bombs. This is the purpose of the start function.
First, it generates a list of -1s and 0s in accordance with the number of bombs and squares on the board, taking into consideration the number of predetermined blanks surrounding the start square. It shuffles that list then inserts the pre-determined blank squares. It then places fills in Board.map with these bomb locations and increments all squares surrounding each bomb. After that the player is ready to go.
##### Board.reset():
If the player finishes a game and wishes to play again they must reset the game. This function sets all values to their default state.
##### Board.checkSquare(toCheck):
This is the function that actually checks a square to see if it is a bomb. For player convience it has been implimented to clear all squares around any discovered 0s, it does this recursivly for all 0s it finds using the _checkSquare() function. It also checks win and loss conditions and maintains the known information in the board.
## Playing the Game
The file game.py uses the pygame library to create a ui to play the game. You left-click to reveal a square and right-click to mark a suspected bomb. Most of the interesting stuff just goes back to the underlying logic, the rest is a pretty simple UI.
## Solver
In Progress
