import chess
import pygame as pg
from time import time, sleep
from moviepy.editor import VideoFileClip
import tkinter as tk

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
    king_square = board.king(board.turn)
    for square in chess.SQUARES:
        if chess.square_distance(king_square, square) <= 1:
            piece = board.piece_at(square)
            if piece and piece.color == board.turn:
                king_safety_score += 1
    for square in chess.SQUARES:
        if chess.square_distance(king_square, square) <= 1:
            piece = board.piece_at(square)
            if piece and piece.color != board.turn:
                king_safety_score -= 1
    return king_safety_score

def evaluate_pawn_structure(board):
    W_connected = 10
    W_isolated = -15
    W_doubled = -20
    W_advanced = 5
    W_backward = -10
    W_hanging = -5
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
            if color == chess.WHITE:
                for rank in ranks:
                    if rank < 5:
                        backward_pawns += 1
            else:
                for rank in ranks:
                    if rank > 3:
                        backward_pawns += 1
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
    safety_score = 0
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 1000
    }
    
    def is_under_attack(board, square, color):
        opponent_color = chess.WHITE if color == chess.BLACK else chess.BLACK
        return board.is_attacked_by(opponent_color, square)

    def is_defended(board, square, color):
        for move in board.legal_moves:
            if move.to_square == square and board.piece_at(move.from_square).color == color:
                return True
        return False
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        color = piece.color
        value = piece_values.get(piece.piece_type, 0)
        under_attack = is_under_attack(board, square, color)
        if piece.piece_type == chess.KING:
            if under_attack:
                safety_score -= 50
            else:
                safety_score += 50
        if piece.piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            if not is_defended(board, square, color) and under_attack:
                safety_score -= value * 2
            if piece.piece_type in [chess.QUEEN, chess.ROOK]:
                if under_attack:
                    safety_score -= value * 1.5
            elif piece.piece_type == chess.PAWN:
                if under_attack and not is_defended(board, square, color):
                    safety_score -= value * 1.5
        if not under_attack:
            if piece.piece_type == chess.PAWN:
                if 8 <= square <= 15:
                    safety_score += value
                elif square % 8 == 0 or (square + 1) % 8 == 0:
                    safety_score += value * 0.5
            elif piece.piece_type == chess.KNIGHT:
                if square in [27, 28, 35, 36]:
                    safety_score += value * 1.2
                else:
                    safety_score += value * 0.8
            elif piece.piece_type in [chess.ROOK, chess.QUEEN]:
                if 27 <= square <= 36:
                    safety_score += value * 1.1
    return safety_score

def evaluate_piece_mobility(board):
    mobility_score = 0
    for piece in board.piece_map().values():
        if piece.color == board.turn:
            mobility_score += len(list(board.legal_moves))
    return mobility_score

def evaluate_passed_pawns(board):
    passed_pawn_score = 0
    for square in board.pieces(chess.PAWN, board.turn):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if board.turn == chess.WHITE:
            if not board.piece_at(chess.square(file, rank + 1)) and not board.piece_at(chess.square(file - 1, rank + 1)) and not board.piece_at(chess.square(file + 1, rank + 1)):
                passed_pawn_score += 1
        else:
            if not board.piece_at(chess.square(file, rank - 1)) and not board.piece_at(chess.square(file - 1, rank - 1)) and not board.piece_at(chess.square(file + 1, rank - 1)):
                passed_pawn_score += 1
    return passed_pawn_score

def determine_game_phase(board):
    piece_count = len(board.pieces(chess.PAWN, chess.WHITE)) + len(board.pieces(chess.PAWN, chess.BLACK)) \
                + len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.KNIGHT, chess.BLACK)) \
                + len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.BLACK)) \
                + len(board.pieces(chess.ROOK, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.BLACK)) \
                + len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
    if piece_count > 16:
        return "opening"
    elif piece_count > 8:
        return "middlegame"
    else:
        return "endgame"

def evaluate_board(board):
    """Generalized board evaluation function with phase-dependent weights."""
    # Define evaluation components and their weights for each phase
    phase_weights = {
        'opening': {
            'piece_value': 1.5,
            'piece_safety': 1.0,
            'position_value': 0.8,
            'center_control': 1.0,
            'king_safety': 0.0,
            'passed_pawns': 0.0
        },
        'midgame': {
            'piece_value': 1.2,
            'piece_safety': 1.0,
            'position_value': 1.0,
            'center_control': 0.7,
            'king_safety': 0.5,
            'passed_pawns': 0.3
        },
        'endgame': {
            'piece_value': 1.0,
            'piece_safety': 0.8,
            'position_value': 0.6,
            'center_control': 0.2,
            'king_safety': 0.6,
            'passed_pawns': 1.2
        }
    }
    
    phase = determine_game_phase(board)
    weights = phase_weights.get(phase, phase_weights['midgame'])  # Default to midgame
    
    # Evaluation components mapping to their functions
    evaluators = {
        'piece_value': piece_values_checker,
        'piece_safety': piece_safety,
        'position_value': piece_position_value,
        'center_control': center_control,
        'king_safety': evaluate_king_safety,
        'passed_pawns': evaluate_passed_pawns
    }
    
    # Calculate weighted score
    score = 0
    for component, weight in weights.items():
        if weight > 0:  # Only evaluate if weight is positive
            evaluator = evaluators[component]
            score += weight * evaluator(board)
    
    return score

def minimax(board, depth, alpha, beta, maximizing_player, start_time, max_time=20):
    if depth == 0 or board.is_game_over() or (time() - start_time > max_time):
        return evaluate_board(board)
    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False, start_time, max_time)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True, start_time, max_time)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth = 16):
    start_time = time()
    best_move = None
    best_score = float('-inf')
    legal_moves = list(board.legal_moves)
    for move in legal_moves:
        print(move)
        board.push(move)
        move_score = minimax(board, depth - 1, float('-inf'), float('inf'), False,start_time)
        board.pop()
        if move_score > best_score:
            best_score = move_score
            best_move = move
    return best_move

def play_best_ai_move(board, screen):
    global running
    c_m_f = False
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
        return
    elif board.is_check() and not c_m_f:
        color = 'black' if board.turn == chess.BLACK else 'white'
        screen.blit(pg.image.load(rf"pic/{color}_king_is_in_check.png"), (0, 0))
        pg.mixer.music.load(r"voc/کیش.mp3")
        pg.display.update()
        pg.mixer.music.play()
        sleep(2)
        draw_board(screen)
        draw_pieces(board, screen)
        c_m_f = True
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
                    for move in board.legal_moves:
                        if move.from_square == chess.square(x_s // 80, 7 - (y_s // 80)):
                            if board.piece_at(move.to_square):
                                pg.draw.rect(screen, (255, 0, 0), ((move.to_square % 8 * 80, (7 - move.to_square // 8) * 80), (80, 80)),5)
                            else:
                                pg.draw.rect(screen, (0, 0, 255), ((move.to_square % 8 * 80, (7 - move.to_square // 8) * 80), (80, 80)),5)
                    pg.display.update()
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
                            screen.blit(pg.image.load(r"pic\wrong_move.png"),(0,0))
                            pg.display.update()
                            sleep(1)
                            draw_board(screen)
                            draw_pieces(board,screen)
                            start_square = end_square = None
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
