import pygame
import random

# Initialize Pygame
pygame.font.init()

# Global constants
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
ROWS, COLS = HEIGHT // BLOCK_SIZE, WIDTH // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
MAGENTA = (255, 0, 255)

# Tetromino shapes
SHAPES = [
    [[[1, 1, 1, 1]]],  # I
    [[[1, 1, 1], [0, 0, 1]]],  # J
    [[[1, 1, 1], [1, 0, 0]]],  # L
    [[[1, 1], [1, 1]]],  # O
    [[[0, 1, 1], [1, 1, 0]]],  # S
    [[[0, 1, 0], [1, 1, 1]]],  # T
    [[[1, 1, 0], [0, 1, 1]]]   # Z
]

# Initialize the display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Class to represent each Tetromino
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice([CYAN, BLUE, ORANGE, YELLOW, GREEN, RED, MAGENTA])
        self.rotation = 0

    def image(self):
        return self.shape[self.rotation % len(self.shape)]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)

# Function to draw the grid
def draw_grid(surface):
    for x in range(COLS):
        for y in range(ROWS):
            pygame.draw.rect(surface, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

# Function to draw the current piece
def draw_piece(surface, piece):
    shape = piece.image()
    for i, row in enumerate(shape):
        for j, val in enumerate(row):
            if val:
                pygame.draw.rect(surface, piece.color, (piece.x * BLOCK_SIZE + j * BLOCK_SIZE, piece.y * BLOCK_SIZE + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Function to check for collision
def check_collision(board, piece):
    for i, row in enumerate(piece.image()):
        for j, val in enumerate(row):
            if val:
                if (piece.x + j < 0 or piece.x + j >= COLS or piece.y + i >= ROWS or board[piece.y + i][piece.x + j]):
                    return True
    return False

# Function to merge the piece into the board
def merge(board, piece):
    for i, row in enumerate(piece.image()):
        for j, val in enumerate(row):
            if val:
                board[piece.y + i][piece.x + j] = piece.color

# Function to clear completed lines
def clear_lines(board):
    lines_cleared = 0
    for i in range(ROWS - 1, -1, -1):
        if all(board[i]):
            del board[i]
            board.insert(0, [BLACK] * COLS)
            lines_cleared += 1
    return lines_cleared

# Function to draw the game over screen
def draw_game_over(surface):
    font = pygame.font.SysFont('Arial', 40)
    text = font.render('Game Over!', True, WHITE)
    surface.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

# Main function to run the game
def main():
    clock = pygame.time.Clock()
    run = True
    board = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
    
    # Start the current piece higher up
    current_piece = Piece(5, 0, random.choice(SHAPES))

    while run:
        clock.tick(10)  # Control the speed of the game
        win.fill(BLACK)  # Clear the screen
        draw_grid(win)  # Draw the grid
        draw_piece(win, current_piece)  # Draw the current piece

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if check_collision(board, current_piece):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if check_collision(board, current_piece):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if check_collision(board, current_piece):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if check_collision(board, current_piece):
                        current_piece.rotate()  # Rotate back if collision

        current_piece.y += 1  # Move the piece down
        if check_collision(board, current_piece):
            current_piece.y -= 1
            merge(board, current_piece)
            clear_lines(board)
            current_piece = Piece(5, 0, random.choice(SHAPES))
            if check_collision(board, current_piece):
                draw_game_over(win)
                pygame.display.update()
                pygame.time.delay(2000)  # Delay to show the game over message for 2 seconds
                run = False

        # Draw the board
        for i in range(ROWS):
            for j in range(COLS):
                pygame.draw.rect(win, board[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.update()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()