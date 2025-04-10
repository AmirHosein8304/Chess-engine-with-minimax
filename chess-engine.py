import chess
import pygame as pg
from time import time, sleep
from moviepy.editor import VideoFileClip
import tkinter as tk
from numpy import inf

def draw_board(screen):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                color = (240, 230, 140)
            else:
                color = (104, 45, 4)
            pg.draw.rect(screen, color, (i * 80, j * 80, 80, 80))

def draw_pieces(board,screen):
    for i in range(8):
        for j in range(8):
            piece = board.piece_at(chess.square(i, 7 - j))
            if piece:
                if piece.color == chess.WHITE:
                    piece_image = pg.image.load(rf"pic/{'w'+piece.symbol()}.png")
                    screen.blit(piece_image, (i * 80, j * 80))
                else:
                    piece_image = pg.image.load(rf"pic/{'b'+piece.symbol()}.png")
                    screen.blit(piece_image, (i * 80, j * 80))
    pg.display.update()

def place_queen(st_sq,en_sq,root,board,screen):
    def inner():
        global move
        root.destroy()
        move = chess.Move(st_sq, en_sq, promotion=chess.QUEEN)
        board.push(move)
        draw_board(screen)
        draw_pieces(board, screen)
        play_best_ai_move(board,screen)
    return inner

def place_rook(st_sq, en_sq, root,board,screen):
    def inner():
        global move
        root.destroy()
        move = chess.Move(st_sq, en_sq, promotion=chess.ROOK)
        board.push(move)
        draw_board(screen)
        draw_pieces(board, screen)
        play_best_ai_move(board,screen)
    return inner

def place_knight(st_sq, en_sq, root,board,screen):
    def inner():
        global move
        root.destroy()
        move = chess.Move(st_sq, en_sq, promotion=chess.KNIGHT)
        board.push(move)
        draw_board(screen)
        draw_pieces(board, screen)
        play_best_ai_move(board,screen)
    return inner

def place_bishop(st_sq, en_sq, root,board,screen):
    def inner():
        global move
        root.destroy()
        move = chess.Move(st_sq, en_sq, promotion=chess.BISHOP)
        board.push(move)
        draw_board(screen)
        draw_pieces(board, screen)
        play_best_ai_move(board,screen)
    return inner

def promote_pawn(st_sq,en_sq,board,screen):
    message_root = tk.Tk()
    message_root.geometry("400x400")
    message_root.config(bg="khaki")
    messag = tk.Label(text="What kind of peices do you want?", bg="khaki", font=("Comic Sans MS", 18),fg="#0000FF")
    messag.place(x=10, y=10)
    queen_button = tk.Button(bg="khaki", fg="#0000FF", text="Queen", font=("Comic Sans MS", 18), width=25,command=place_queen(st_sq,en_sq,message_root,board,screen))
    queen_button.place(x=10, y=50)
    rook_button = tk.Button(bg="khaki", fg="#0000FF", text="Rook", font=("Comic Sans MS", 18), width=25,command=place_rook(st_sq,en_sq,message_root,board,screen))
    rook_button.place(x=10, y=125)
    knight_button = tk.Button(bg="khaki", fg="#0000FF", text="Knight", font=("Comic Sans MS", 18), width=25,command=place_knight(st_sq,en_sq,message_root,board,screen))
    knight_button.place(x=10, y=200)
    bishop_button = tk.Button(bg="khaki", fg="#0000FF", text="Bishop", font=("Comic Sans MS", 18), width=25,command=place_bishop(st_sq,en_sq,message_root,board,screen))
    bishop_button.place(x=10, y=275)
    message_root.mainloop()

def piece_position_value(board):
    piece_pos_val = {
        chess.PAWN:
            [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0.5, 1, 1, -2, -2, 1, 1, 0.5],
                [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
                [0, 0, 0, 2, 2, 0, 0, 0],
                [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [5, 5, 5, 5, 5, 5, 5, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
        chess.KNIGHT:
            [
                [-5, -4, -3, -3, -3, -3, -4, -5,],
                [-4, -2, 0, 0.5, 0.5, 0, -2, -4,],
                [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,],
                [-3, 0, 1.5, 2, 2, 1.5, 0, -3,],
                [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,],
                [-3, 0, 1, 1.5, 1.5, 1, 0, -3,],
                [-4, -2, 0, 0, 0, 0, -2, -4,],
                [-5, -4, -3, -3, -3, -3, -4, -5],
            ],
        chess.BISHOP:
            [
                [-2, -1, -1, -1, -1, -1, -1, -2,],
                [-1, 0.5, 0, 0, 0, 0, 0.5, -1,],
                [-1, 1, 1, 1, 1, 1, 1, -1,],
                [-1, 0, 1, 1, 1, 1, 0, -1,],
                [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,],
                [-1, 0, 0.5, 1, 1, 0.5, 0, -1,],
                [-1, 0, 0, 0, 0, 0, 0, -1,],
                [-2, -1, -1, -1, -1, -1, -1, -2],
            ],
        chess.ROOK:
            [
                [0, 0, 0, 0.5, 0.5, 0, 0, 0],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5,],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5,],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5,],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5,],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5,],
                [0.5, 1, 1, 1, 1, 1, 1, 0.5,],
                [0, 0, 0, 0, 0, 0, 0, 0,],
            ],
        chess.QUEEN:
            [
                [-2, -1, -1, -0.5, -0.5, -1, -1, -2,],
                [-1, 0, 0, 0, 0, 0, 0, -1,],
                [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,],
                [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,],
                [0.0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,],
                [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,],
                [-1, 0, 0.5, 0, 0, 0, 0, -1,],
                [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
            ],
        chess.KING:
            [
                [-3, -4, -4, -5, -5, -4, -4, -3,],
                [-3, -4, -4, -5, -5, -4, -4, -3,],
                [-3, -4, -4, -5, -5, -4, -4, -3,],
                [-3, -4, -4, -5, -5, -4, -4, -3,],
                [-2, -3, -3, -4, -4, -3, -3, -2],
                [-1, -2, -2, -2, -2, -2, -2, -1],
                [2, 2, 0, 0, 0, 0, 2, 2],
                [2, 3, 1, 0, 0, 1, 3, 2]
            ]}
    s_val = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.BLACK:
                s_val += piece_pos_val[piece.piece_type][7 - chess.square_rank(square)][chess.square_file(square)]
            else:
                s_val -= piece_pos_val[piece.piece_type][7 - chess.square_rank(square)][chess.square_file(square)]
    return s_val

def evaluate_black_targeted_squares(board):
    black_targeted = set()
    for move in board.legal_moves:
        if not board.piece_at(move.from_square) or board.piece_at(move.from_square).color == chess.BLACK:
            black_targeted.add(move.to_square)
    return len(black_targeted)

def evaluate_forks(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3.5,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  
    }

    fork_score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece and piece.color == chess.BLACK:  
            attacked_squares = board.attacks(square)
            targeted_pieces = []

            for attacked_square in attacked_squares:
                target = board.piece_at(attacked_square)
                if target and target.color == chess.WHITE:  
                    targeted_pieces.append(target)

            if len(targeted_pieces) >= 2:  
                fork_value = sum(piece_values[target.piece_type] for target in targeted_pieces)
                fork_score += fork_value

    return fork_score

def square_target_with_piece_values(board, square, weight=2):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    
    allied_target_score = 0
    enemy_target_score = 0

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            legal_moves = board.attacks(sq)
            if square in legal_moves:
                piece_value = piece_values[piece.piece_type]
                if piece.color == board.turn:
                    allied_target_score += piece_value
                else: 
                    enemy_target_score += piece_value

    score = (allied_target_score - enemy_target_score) * weight
    return score

def piece_values_checker(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0 
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

def center_control(board):
    center_squares = {chess.D4, chess.D5, chess.E4, chess.E5}
    center_control_point = 10  
    score = 0
    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                score += center_control_point
            else:
                score -= center_control_point
    return score

def evaluate_king_safety(board):
    king_safety_score = 0
    king_square = board.king(board.turn)  # Get the king's position
    
    # Check surrounding squares (8 squares around the king)
    for square in chess.SQUARES:
        if chess.square_distance(king_square, square) <= 1:  # Check neighboring squares
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                king_safety_score += 1  # Count protected squares

    # Penalize for exposed kings (opponent's pieces near the king)
    for square in chess.SQUARES:
        if chess.square_distance(king_square, square) <= 1:
            piece = board.piece_at(square)
            if piece and piece.color != board.turn:
                king_safety_score -= 1  # Penalize for opponent's influence around the king
    
    return king_safety_score

def evaluate_pawn_structure(board):
    W_connected = 10
    W_isolated = -15
    W_doubled = -20
    W_advanced = 5
    W_backward = -10  # Penalize for backward pawns
    W_hanging = -5    # Penalize for hanging pawns

    score = 0

    for color in [chess.WHITE, chess.BLACK]:
        pawn_files = {}
        isolated_pawns = 0
        doubled_pawns = 0
        connected_pawns = 0
        advanced_pawns = 0
        backward_pawns = 0
        hanging_pawns = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN and piece.color == color:
                file_index = chess.square_file(square)
                rank_index = chess.square_rank(square)

                if file_index in pawn_files:
                    pawn_files[file_index].append(rank_index)
                else:
                    pawn_files[file_index] = [rank_index]

                if (color == chess.WHITE and rank_index >= 4) or (color == chess.BLACK and rank_index <= 3):
                    advanced_pawns += 1

        for file_index, ranks in pawn_files.items():
            ranks.sort()
            if len(ranks) > 1:
                doubled_pawns += (len(ranks) - 1)

            if (file_index - 1 not in pawn_files) and (file_index + 1 not in pawn_files):
                isolated_pawns += len(ranks)

            if (file_index - 1 in pawn_files or file_index + 1 in pawn_files):
                connected_pawns += len(ranks)

            # Detect backward pawns (pawns on an open file, unable to advance)
            if color == chess.WHITE:
                for rank in ranks:
                    if rank < 5:
                        backward_pawns += 1
            else:
                for rank in ranks:
                    if rank > 3:
                        backward_pawns += 1

            # Detect hanging pawns (pawns not supported by another pawn)
            if color == chess.WHITE:
                for rank in ranks:
                    if not board.piece_at(chess.square(file_index - 1, rank)) and not board.piece_at(chess.square(file_index + 1, rank)):
                        hanging_pawns += 1
            else:
                for rank in ranks:
                    if not board.piece_at(chess.square(file_index - 1, rank)) and not board.piece_at(chess.square(file_index + 1, rank)):
                        hanging_pawns += 1

        pawn_structure_score = (
            (connected_pawns * W_connected) -
            (isolated_pawns * W_isolated) -
            (doubled_pawns * W_doubled) +
            (advanced_pawns * W_advanced) -
            (backward_pawns * W_backward) -
            (hanging_pawns * W_hanging)
        )

        if color == chess.WHITE:
            score += pawn_structure_score
        else:
            score -= pawn_structure_score

    return score

def piece_safety(board):
    """Evaluates the safety of all pieces and returns a safety score."""
    safety_score = 0
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 1000  # King has high value as it cannot be captured
    }
    
    def is_under_attack(board, square, color):
        """Returns True if the square is under attack by the opponent."""
        opponent_color = chess.WHITE if color == chess.BLACK else chess.BLACK
        return board.is_attacked_by(opponent_color, square)

    def is_defended(board, square, color):
        """Returns True if the piece is defended by another piece of the same color."""
        for move in board.legal_moves:
            if move.to_square == square and board.piece_at(move.from_square).color == color:
                return True
        return False

    # Evaluate each piece on the board
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue

        color = piece.color
        value = piece_values.get(piece.piece_type, 0)
        
        # Check if the piece is under attack
        under_attack = is_under_attack(board, square, color)
        
        # Safety for the King: King's safety is paramount.
        if piece.piece_type == chess.KING:
            if under_attack:
                safety_score -= 50  # Severe penalty if the King is under attack
            else:
                safety_score += 50  # Reward if the King is safe
                
        # Check for piece exposure and mobility
        if piece.piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            # A piece is considered "exposed" if it is not defended by another piece
            if not is_defended(board, square, color) and under_attack:
                # Penalize for an exposed piece under attack
                safety_score -= value * 2  # Higher penalty for exposed pieces
                
            # High-value pieces (like Queen, Rook) should be more cautious in the middle game
            if piece.piece_type in [chess.QUEEN, chess.ROOK]:
                if under_attack:
                    safety_score -= value * 1.5  # High-value pieces under attack are highly penalized
            elif piece.piece_type == chess.PAWN:
                # Pawns are safer when they are supported by another pawn or piece
                if under_attack and not is_defended(board, square, color):
                    safety_score -= value * 1.5  # Penalize for isolated pawns being attacked

        # Add score for unthreatened piece positions
        if not under_attack:
            if piece.piece_type == chess.PAWN:
                # Pawns are usually safest in the back ranks or behind other pawns
                if 8 <= square <= 15:  # Back-rank pawns
                    safety_score += value  # Reward back-rank pawns
                elif square % 8 == 0 or (square + 1) % 8 == 0:  # Pawns on the edges
                    safety_score += value * 0.5  # Penalize edge pawns slightly

            elif piece.piece_type == chess.KNIGHT:
                # Knights are safer when they are near the center or protected
                if square in [27, 28, 35, 36]:  # Central squares for knights
                    safety_score += value * 1.2
                else:
                    safety_score += value * 0.8
            
            # Rooks and queens are safer in more controlled positions, especially near the center
            elif piece.piece_type in [chess.ROOK, chess.QUEEN]:
                if 27 <= square <= 36:  # Central area
                    safety_score += value * 1.1  # Reward central placement for rooks/queens

    return safety_score

def evaluate_piece_mobility(board):
    mobility_score = 0
    for piece in board.piece_map().values():
        if piece.color == board.turn:  # Evaluate only for the current player's pieces
            mobility_score += len(list(board.legal_moves))  # Count legal moves
    return mobility_score

def evaluate_passed_pawns(board):
    passed_pawn_score = 0
    for square in board.pieces(chess.PAWN, board.turn):
        # Check if it's a passed pawn (no opponent pawns on its file or adjacent files)
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        
        if board.turn == chess.WHITE:
            # For white, we check if there are no black pawns on the same file or adjacent files
            if not board.piece_at(chess.square(file, rank + 1)) and not board.piece_at(chess.square(file - 1, rank + 1)) and not board.piece_at(chess.square(file + 1, rank + 1)):
                passed_pawn_score += 1  # Give value to the passed pawn
        else:
            # For black, we check if there are no white pawns on the same file or adjacent files
            if not board.piece_at(chess.square(file, rank - 1)) and not board.piece_at(chess.square(file - 1, rank - 1)) and not board.piece_at(chess.square(file + 1, rank - 1)):
                passed_pawn_score += 1  # Give value to the passed pawn
    
    return passed_pawn_score

def determine_game_phase(board):
    """Determines the phase of the game: opening, middlegame, or endgame."""
    piece_count = len(board.pieces(chess.PAWN, chess.WHITE)) + len(board.pieces(chess.PAWN, chess.BLACK)) \
                + len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.KNIGHT, chess.BLACK)) \
                + len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.BLACK)) \
                + len(board.pieces(chess.ROOK, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.BLACK)) \
                + len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))

    # More pieces on the board means opening/middlegame, fewer pieces indicate endgame
    if piece_count > 16:
        return "opening"
    elif piece_count > 8:
        return "middlegame"
    else:
        return "endgame"
        
def evaluate_board(board):
    score = 0
    phase = determine_game_phase(board)  # Determine if it's opening, midgame, or endgame

    if phase == 'opening':
        score += 1.5 * piece_values_checker(board)  # More importance to piece value in the opening
        score += 1.0 * piece_safety(board)
        score += 0.8 * piece_position_value(board)
        score += 1.0 * center_control(board)
    elif phase == 'midgame':
        score += 1.2 * piece_values_checker(board)  # Balanced evaluation for midgame
        score += 1.0 * piece_safety(board)
        score += 1.0 * piece_position_value(board)
        score += 0.7 * center_control(board)
    else:  # endgame
        score += 1.0 * piece_values_checker(board)  # Fewer pieces on the board, so value is different
        score += 0.8 * piece_safety(board)
        score += 0.6 * evaluate_king_safety(board)  # King safety becomes more critical in the endgame
        score += 1.2 * evaluate_passed_pawns(board)  # Passed pawns are critical in the endgame
    return score

def piece_value(piece):
    """Return the value of the piece based on its type."""
    if piece is None:
        return 0
    if piece.piece_type == chess.PAWN:
        return 1
    elif piece.piece_type == chess.KNIGHT:
        return 3
    elif piece.piece_type == chess.BISHOP:
        return 3
    elif piece.piece_type == chess.ROOK:
        return 5
    elif piece.piece_type == chess.QUEEN:
        return 9
    elif piece.piece_type == chess.KING:
        return 1000  # King is critical
    return 0

def evaluate_move(move, board):
    """Evaluate the move based on its potential value, including if it puts a piece in danger."""
    score = 0
    
    # 1. Check if the move is a capture
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        score += piece_value(captured_piece)  # Reward for capturing a piece
    
    # 2. Check if the move puts the piece in danger (i.e., the square is attacked by the opponent)
    opponent_color = chess.BLACK if board.turn == chess.WHITE else chess.WHITE  # Determine the opponent's color
    if board.is_attacked_by(opponent_color, move.to_square):  # Check if the opponent can attack the square
        score -= 10  # Penalize for putting the piece in danger
    
    # 3. Check if the move helps in defense (i.e., if the player is defending the target square)
    defending_pieces = []
    # Iterate over all pieces of the current player
    for piece in board.pieces(chess.PAWN, board.turn):  # Iterate over pawns first
        for legal_move in board.legal_moves:
            if legal_move.from_square == piece and legal_move.to_square == move.to_square:
                defending_pieces.append(piece)
    
    for piece in board.pieces(chess.KNIGHT, board.turn):  # Repeat for other piece types
        for legal_move in board.legal_moves:
            if legal_move.from_square == piece and legal_move.to_square == move.to_square:
                defending_pieces.append(piece)
                
    for piece in board.pieces(chess.BISHOP, board.turn):
        for legal_move in board.legal_moves:
            if legal_move.from_square == piece and legal_move.to_square == move.to_square:
                defending_pieces.append(piece)
    
    for piece in board.pieces(chess.ROOK, board.turn):
        for legal_move in board.legal_moves:
            if legal_move.from_square == piece and legal_move.to_square == move.to_square:
                defending_pieces.append(piece)
    
    for piece in board.pieces(chess.QUEEN, board.turn):
        for legal_move in board.legal_moves:
            if legal_move.from_square == piece and legal_move.to_square == move.to_square:
                defending_pieces.append(piece)

    if defending_pieces:
        score += 5  # Reward if the move defends an important piece

    return score

def find_best_move(board):
    start_time = time()
    best_move = None
    best_score = -inf
    for move in board.legal_moves:
        if time()-start_time>=100:
            break
        board.push(move)
        move_score = value(board, False, -inf, inf)
        board.pop()
        if best_move is None or move_score > best_score:
            best_move = move
            best_score = move_score
    return best_move

def play_best_ai_move(board, screen):
    starttime = time()
    global running
    if board.is_checkmate():
        color = 'black' if board.turn == chess.BLACK else 'white'
        for i in range(8):
            for j in range(8):
                piece = board.piece_at(chess.square(i, 7 - j))
                if piece and piece.piece_type == chess.KING and piece.color == board.turn:
                    screen.blit(pg.image.load(r"pic/check_block.png"), (i * 80, j * 80))
                    pg.mixer.music.load(r"voc/مات.mp3")
                    pg.display.update()
                    pg.mixer.music.play()
                    sleep(2)
        pg.display.set_caption('Checkmate!')
        clip = VideoFileClip(r'voc/checkmate.mp4')
        clip.preview()
        pg.quit()
        screen = pg.display.set_mode((640, 640))
        pg.display.set_caption('Game Over!')
        screen.blit(pg.image.load(rf"pic/{color}_lost.png"), (0, 0))
        pg.display.update()
        sleep(1)
        root = tk.Tk()
        root.title('Play again?')
        root.eval('tk::PlaceWindow . center')
        root.geometry('500x100')
        message = tk.Label(root, text='Game Over! Do you want to play again?', font=("Comic Sans MS", 18))
        message.place(x=30, y=0)
        no_button = tk.Button(root, text='No', font=("Comic Sans MS", 18), command=root.destroy)
        no_button.place(x=100, y=50)
        yes_button = tk.Button(root, text='Yes', font=("Comic Sans MS", 18), command=play_again(root))
        yes_button.place(x=300, y=50)
        root.mainloop()
        running = False
        print(time() - starttime)
        return
    best_move = find_best_move(board)
    if best_move:
        r_piece = board.piece_at(best_move.to_square)
        board.push(best_move)
        c_m_f = False
        draw_board(screen)
        draw_pieces(board, screen)
        if r_piece:
            pg.mixer.music.load(r"voc/حذف مهره.mp3")
        else:
            pg.mixer.music.load(r"voc/گذاشتن مهره.mp3")
        pg.mixer.music.play()

def value(board, is_maximizing, alpha, beta, depth = 0, start_time = None):
    print(depth)
    if depth==0:
        start_time = time()
    result = board.result()
    if result == "1-0" or result=="0-1":
        return evaluate_board(board)
    elif result == "1/2-1/2":
        return 0

    if is_maximizing and depth!=16:
        return max_value(board, alpha, beta, depth, start_time)
    elif not is_maximizing and depth!=16:
        return min_value(board, alpha, beta, depth, start_time)
    elif depth==16:
        return evaluate_board(board)

def max_value(board, alpha, beta, depth, start_time):
    if board.is_game_over() or depth==16 or time()-start_time>=100:
        return evaluate_board(board)
    
    v = -inf
    for move in board.legal_moves:
        board.push(move)
        v = max(v, value(board, False, alpha, beta,depth+1, start_time))
        board.pop()
        if v>=beta:
            return v
        alpha = max(alpha, v)
    return v

def min_value(board, alpha, beta, depth, start_time):
    if board.is_game_over() or depth==16 or time()-start_time>=100:
        return evaluate_board(board)
    
    v = inf
    for move in board.legal_moves:
        board.push(move)
        v = min(v, value(board, True, alpha, beta, depth+1, start_time))
        board.pop()
        if v<=alpha:
            return v
        beta = min(beta, v)
    return v

def play_again(root):
    def inner():
        root.destroy()
        main()
    return inner

def main():
    pg.init()
    screen = pg.display.set_mode((640, 640))
    pg.display.set_caption("Chess")
    pg.mixer.music.load(r"voc/war_horn_3.mp3")
    screen.blit(pg.image.load(r"pic/welcome_page.png"), (0, 0))
    pg.display.update()
    pg.mixer.music.play()
    sleep(2)

    board = chess.Board()
    running = True
    counter = 0
    c_m_f = False
    draw_board(screen)
    draw_pieces(board, screen)

    while running:
        for event in pg.event.get():
            if board.is_checkmate():
                color = 'black' if board.turn == chess.BLACK else 'white'
                for i in range(8):
                    for j in range(8):
                        piece = board.piece_at(chess.square(i, 7 - j))
                        if piece and piece.piece_type == chess.KING and piece.color == board.turn:
                            screen.blit(pg.image.load(r"pic/check_block.png"), (i * 80, j * 80))
                            pg.mixer.music.load(r"voc/مات.mp3")
                            pg.display.update()
                            pg.mixer.music.play()
                            sleep(2)
                pg.display.set_caption('Checkmate!')
                clip = VideoFileClip('checkmate.mp4')
                clip.preview()

                pg.quit()
                screen = pg.display.set_mode((640, 640))
                pg.display.set_caption('Game Over!')
                screen.blit(pg.image.load(rf"pic/{color}_lost.png"), (0, 0))
                pg.display.update()
                sleep(1)

                root = tk.Tk()
                root.title('Play again?')
                root.eval('tk::PlaceWindow . center')
                root.geometry('500x100')
                message = tk.Label(root, text='Game Over! Do you want to play again?', font=("Comic Sans MS", 18))
                message.place(x=30, y=0)
                no_button = tk.Button(root, text='No', font=("Comic Sans MS", 18), command=root.destroy)
                no_button.place(x=100, y=50)
                yes_button = tk.Button(root, text='Yes', font=("Comic Sans MS", 18), command=lambda: play_again(root))
                yes_button.place(x=300, y=50)
                root.mainloop()

                running = False

            elif board.is_check() and not c_m_f:
                draw_board(screen)
                draw_pieces(board, screen)
                pg.display.update()
                sleep(1.5)
                color = 'black' if board.turn == chess.BLACK else 'white'
                screen.blit(pg.image.load(rf"pic/{color}_king_is_in_check.png"), (0, 0))
                pg.mixer.music.load(r"voc/کیش.mp3")
                pg.display.update()
                pg.mixer.music.play()
                sleep(2)
                draw_board(screen)
                draw_pieces(board, screen)
                c_m_f = True

            elif board.is_stalemate():
                screen.blit(pg.image.load(rf"pic/stalemate.png"), (0, 0))
                pg.display.update()
                sleep(1)
                running = False

            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if counter % 2 == 0:
                    x_s, y_s = pg.mouse.get_pos()
                    piece = board.piece_at(chess.square(x_s // 80, 7 - (y_s // 80)))
                    if piece and piece.color == board.turn:
                        counter = counter + 1
                    else:
                        continue
                else:
                    x_e, y_e = pg.mouse.get_pos()
                    counter = counter + 1
                    if counter >= 2:
                        start_square = chess.square(x_s // 80, 7 - (y_s // 80))
                        end_square = chess.square(x_e // 80, 7 - (y_e // 80))
                        s_piece = board.piece_at(start_square)
                        try:
                            move = board.find_move(start_square, end_square)
                        except:
                            continue

                        if s_piece and move in board.legal_moves and s_piece.piece_type == chess.PAWN and (end_square // 8 == 0 or end_square // 8 == 7):
                            promote_pawn(start_square, end_square, board, screen)
                            c_m_f = False
                        elif move in board.legal_moves:
                            r_piece = board.piece_at(end_square)
                            board.push(move)
                            if r_piece:
                                pg.mixer.music.load(r"voc/حذف مهره.mp3")
                                pg.mixer.music.play()
                            else:
                                pg.mixer.music.load(r"voc/گذاشتن مهره.mp3")
                                pg.mixer.music.play()
                            c_m_f = False
                            draw_board(screen)
                            draw_pieces(board, screen)
                            play_best_ai_move(board, screen)

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
