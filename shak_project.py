import pygame
import chess
import chess.engine

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption('Chess AI Game')

# Load chessboard image
board_image = pygame.image.load('chessboard.png')

# Define square size
square_size = 60

# Initialize chess board
board = chess.Board()

def draw_board(screen, board):
    # Draw the chessboard
    screen.blit(board_image, (0, 0))
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            file = chess.FILE_NAMES[chess.square_file(square)]
            rank = chess.RANK_NAMES[chess.square_rank(square)]
            x = square_size * int(file)
            y = square_size * (7 - int(rank))
            piece_image = pygame.image.load(f"{piece.symbol()}.png")
            screen.blit(piece_image, (x, y))

def play_ai_move(board):
    # AI randomly selects a legal move
    import random
    legal_moves = list(board.legal_moves)
    move = random.choice(legal_moves)
    board.push(move)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and board.turn:
            # Player move
            x, y = event.pos
            square = chess.square(x // square_size, 7 - (y // square_size))
            move = chess.Move.from_uci(board.find_move(square))
            if move in board.legal_moves:
                board.push(move)
                play_ai_move(board)
                
    draw_board(screen, board)
    pygame.display.flip()

pygame.quit()
