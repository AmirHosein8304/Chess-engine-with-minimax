import pygame
import chess

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Chess AI Game')

# Load chessboard image
board_image = pygame.image.load('board.png')

# Define square size
square_size = 80

# Initialize chess board
board = chess.Board()

# Mapping chess symbols to filenames (to avoid case-sensitive conflicts)
symbol_to_filename = {
    'p': 'bp.png',  # Black pawn
    'r': 'br.png',  # Black rook
    'n': 'bn.png',  # Black knight
    'b': 'bb.png',  # Black bishop
    'q': 'bq.png',  # Black queen
    'k': 'bk.png',  # Black king
    'P': 'wp.png',  # White pawn
    'R': 'wr.png',  # White rook
    'N': 'wn.png',  # White knight
    'B': 'wb.png',  # White bishop
    'Q': 'wq.png',  # White queen
    'K': 'wk.png',  # White king
}

# Dictionary for piece images
piece_images = {}

# Preload images for chess pieces
for symbol, filename in symbol_to_filename.items():
    try:
        piece_images[symbol] = pygame.image.load(filename)
    except FileNotFoundError:
        print(f"Image for {symbol} ({filename}) not found.")

def draw_board(screen, board, selected_square=None):
    # Draw the chessboard
    screen.blit(board_image, (0, 0))  # Draw the chessboard at the top-left corner
    
    # Highlight the selected square
    if selected_square is not None:
        x = square_size * chess.square_file(selected_square)
        y = square_size * (7 - chess.square_rank(selected_square))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, square_size, square_size), 3)
    
    # Draw the chess pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Calculate the exact position for the piece
            x = square_size * chess.square_file(square)
            y = square_size * (7 - chess.square_rank(square))
            
            # Scale the piece image to fit the square size
            piece_image = piece_images.get(piece.symbol())
            if piece_image:
                piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
                screen.blit(piece_image, (x, y))

def promote_pawn_with_pygame():
    # Create a small `pygame` window to allow the user to choose a promotion piece
    promotion_screen = pygame.Surface((240, 60))
    promotion_screen.fill((200, 200, 200))  # Light gray background

    # Load images for promotion choices
    promotion_pieces = {
        chess.QUEEN: pygame.transform.scale(pygame.image.load("wq.png"), (50, 50)),
        chess.ROOK: pygame.transform.scale(pygame.image.load("wr.png"), (50, 50)),
        chess.BISHOP: pygame.transform.scale(pygame.image.load("wb.png"), (50, 50)),
        chess.KNIGHT: pygame.transform.scale(pygame.image.load("wn.png"), (50, 50)),
    }

    # Draw the promotion pieces on the small screen
    x_offset = 10
    piece_rects = {}
    for piece_type, image in promotion_pieces.items():
        promotion_screen.blit(image, (x_offset, 5))
        piece_rects[piece_type] = pygame.Rect(x_offset, 5, 50, 50)  # Track piece positions
        x_offset += 60  # Add spacing between pieces

    # Display the promotion screen
    screen.blit(promotion_screen, (120, 210))  # Position it centrally on the main window
    pygame.display.flip()

    # Wait for the user to select a piece
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for piece_type, rect in piece_rects.items():
                    if rect.collidepoint(mouse_x - 120, mouse_y - 210):
                        return piece_type  # Return the selected piece type
            elif event.type == pygame.QUIT:
                pygame.quit()
                return None

def evaluate_board(board):
    """
    A simple evaluation function that assigns material values to the pieces:
    Positive values favor White, negative values favor Black.
    """
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # King is invaluable in chess
    }

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

def play_best_ai_move(board):
    """
    AI selects the best move for Black by evaluating all legal moves.
    """
    best_move = None
    best_score = float('inf')  # Since AI is Black, aim for the lowest score

    for move in board.legal_moves:
        board.push(move)
        score = evaluate_board(board)
        board.pop()

        if score < best_score:
            best_score = score
            best_move = move

    if best_move:
        board.push(best_move)

# Game loop variables
running = True
selected_square = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            clicked_square = chess.square(x // square_size, 7 - (y // square_size))

            if selected_square is None:
                # Select a piece
                if board.piece_at(clicked_square) and board.piece_at(clicked_square).color == board.turn:
                    selected_square = clicked_square
            else:
                # Try to make a move
                move = chess.Move(selected_square, clicked_square)

                # Handle pawn promotion
                if (board.piece_at(selected_square).piece_type == chess.PAWN and
                        (chess.square_rank(clicked_square) == 7 or chess.square_rank(clicked_square) == 0)):
                    promotion_choice = promote_pawn_with_pygame()
                    if promotion_choice:
                        move = chess.Move(selected_square, clicked_square, promotion=promotion_choice)

                if move in board.legal_moves:
                    board.push(move)
                    play_best_ai_move(board)

                # Reset selection
                selected_square = None
    
    draw_board(screen, board, selected_square)
    pygame.display.flip()

pygame.quit()
