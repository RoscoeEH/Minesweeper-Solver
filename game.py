# This has the pygame graphics to acually play minesweeper when interfaced with minesweeperLogic.py
# Run this to play the game

import pygame
import pygame.freetype

from minesweeperLogic import Board

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_WIDTH = 5
GRID_HEIGHT = 5
TILE_SIZE = 50
NUM_MINES_START = 3

# Self-explainatory class
# Used for reset button
class Button:
    def __init__(self, text, position, action):
        self.text = text
        self.position = position
        self.action = action
        self.font = pygame.freetype.SysFont(None, 24)
        self.rect = pygame.Rect(self.position, (self.font.get_rect(self.text).width + 10, self.font.get_rect(self.text).height + 10))

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        textSurface, _ = self.font.render(self.text, (0, 0, 0))
        screen.blit(textSurface, (self.position[0] + 5, self.position[1] + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            if self.rect.collidepoint(mouseX, mouseY):
                self.action()

def main():
    pygame.init()

    # Initialize a grid to keep track of cell states (True means cell is filled)
    grid = [[True for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    # Initialize a grid to track red squares (labeled as a bomb by the player)
    redGrid = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    board = Board(GRID_WIDTH, GRID_HEIGHT, NUM_MINES_START)

    # Initialize an array to store mineMap corresponding to the number in each cell
    mineMap = board.map

    # Initialize Pygame font
    pygame.freetype.init()
    font = pygame.freetype.SysFont(None, 24)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Sets the game back to defaut state
    def reset_grid():
        nonlocal gameStarted
        gameStarted = False
        board.reset()
        nonlocal mineMap
        mineMap = board.map
        nonlocal minesRemaining
        minesRemaining = NUM_MINES_START
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                grid[row][col] = True
                redGrid[row][col] = False  # Reset red squares

    # Places reset button
    resetButton = Button("Reset", (SCREEN_WIDTH - 100, 10), reset_grid)

    # minesRemaining variables
    minesRemaining = NUM_MINES_START
    minesRemainingPosition = (SCREEN_WIDTH - 100, 50)  # Position beneath the reset button

    # Stops when the window is exited
    run = True
    # Prevents player from doing anything before board is generated
    gameStarted = False

    while run:

        # Event handler loop
        for event in pygame.event.get():
            # Exit condition
            if event.type == pygame.QUIT:
                run = False

            # Handle resetButton
            resetButton.handle_event(event)
            
            # Handles mouse clicks

            # Only handle other events if the game is not won or lost
            if board.knownCount != 0 and not board.gameLost:  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    gridX = mouseX // TILE_SIZE
                    gridY = mouseY // TILE_SIZE

                    if 0 <= gridX < GRID_WIDTH and 0 <= gridY < GRID_HEIGHT:
                        # Left mouse button click
                        if event.button == 1:
                            if not gameStarted:
                                gameStarted = True
                                board.start(gridX, gridY)
                                mineMap = board.map
                            
                            # Cannot click red squares
                            if not redGrid[gridY][gridX]:
                                for square in board.checkSquare([[gridX, gridY]]):
                                    grid[square[1]][square[0]] = False
                                
                        elif event.button == 3:  # Right mouse button click
                            if gameStarted and grid[gridY][gridX] == True:
                                if not redGrid[gridY][gridX]:
                                    redGrid[gridY][gridX] = True
                                    minesRemaining -= 1
                                else:
                                    redGrid[gridY][gridX] = False
                                    minesRemaining += 1


        # Fill the screen with a background color
        screen.fill((255, 255, 255))

        # Draw the grid and squares with black edges
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
                # Draw black border for each cell
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

                # Determine color based on redGrid
                if redGrid[row][col]:
                    pygame.draw.rect(screen, (255, 0, 0), rect)  # Red color
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black border
                elif grid[row][col]:
                    pygame.draw.rect(screen, (169, 169, 169), rect)  # Grey color
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black border

                # Render number from array centered in the cell if cell is not filled
                if not grid[row][col]:
                    number = mineMap[row][col]
                    textSurface, _ = font.render(str(number), (0, 0, 0))
                    textRect = textSurface.get_rect(center=rect.center)
                    screen.blit(textSurface, textRect)

        # Draw the reset button
        resetButton.draw(screen)

        # Draw countdown number
        minesRemainingText = f"{minesRemaining}"
        minesRemainingSurface, _ = font.render(minesRemainingText, (0, 0, 0))
        screen.blit(minesRemainingSurface, minesRemainingPosition)

        # Draw "You Win" if the game is won
        if board.knownCount == 0:
            winText = "You Win"
            winSurface, _ = font.render(winText, (0, 255, 0))
            winPosition = (SCREEN_WIDTH - 100, 80)
            screen.blit(winSurface, winPosition)

        # Draw "You Lost" if the game is lost
        if board.gameLost:
            loseText = "You Lost"
            loseSurface, _ = font.render(loseText, (255, 0, 0))
            losePosition = (SCREEN_WIDTH - 100, 80)
            screen.blit(loseSurface, losePosition)

        pygame.display.flip()

    pygame.quit()
    pygame.freetype.quit()

if __name__ == "__main__":
    main()
