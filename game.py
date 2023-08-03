import pygame
import random
import time

pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
ROWS, COLS = 6, 6
SQUARE_SIZE = WIDTH // ROWS

# Colors
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Initialize window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match Three")

# Initialize grid
grid = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

# Function to draw the grid
def draw_grid():
    window.fill(WHITE)
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(window, grid[y][x], (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.display.flip()

# Function to check and remove matches
def check_matches():
    found_match = False
    # Check horizontal matches
    for y in range(ROWS):
        for x in range(COLS - 2):
            if grid[y][x] == grid[y][x + 1] == grid[y][x + 2]:
                grid[y][x] = grid[y][x + 1] = grid[y][x + 2] = None
                found_match = True

    # Check vertical matches
    for x in range(COLS):
        for y in range(ROWS - 2):
            if grid[y][x] == grid[y + 1][x] == grid[y + 2][x]:
                grid[y][x] = grid[y + 1][x] = grid[y + 2][x] = None
                found_match = True

    # Drop gems above empty spaces
    for x in range(COLS):
        offset = 0
        for y in reversed(range(ROWS)):
            if grid[y][x] is None:
                offset += 1
            elif offset > 0:
                grid[y + offset][x], grid[y][x] = grid[y][x], None

    # Fill empty spaces with new gems
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x] is None:
                grid[y][x] = random.choice(COLORS)

    return found_match

# Game loop
selected_gem = None
run = True
while run:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
            # Check if a gem is already selected
            if selected_gem:
                prev_row, prev_col = selected_gem
                # If the clicked gem is adjacent to the previously selected one, swap them
                if abs(prev_row - row) + abs(prev_col - col) == 1:
                    grid[prev_row][prev_col], grid[row][col] = grid[row][col], grid[prev_row][prev_col]
                    selected_gem = None
                    # Check if a match has been made
                    if check_matches():
                        time.sleep(0.5)
                        while check_matches():
                            draw_grid()
                            time.sleep(0.5)
                    else: # No match found, so revert the swap
                        grid[prev_row][prev_col], grid[row][col] = grid[row][col], grid[prev_row][prev_col]
                else:
                    selected_gem = (row, col)
            else:
                selected_gem = (row, col)

pygame.quit()
