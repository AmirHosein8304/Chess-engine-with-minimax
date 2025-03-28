import chess
import pygame as pg
import time
import moviepy.editor
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
                    piece_image = pg.image.load(rf"pic\{'w'+piece.symbol()}.png")
                    screen.blit(piece_image, (i * 80, j * 80))
                else:
                    piece_image = pg.image.load(rf"pic\{'b'+piece.symbol()}.png")
                    screen.blit(piece_image, (i * 80, j * 80))

def place_queen(st_sq,en_sq,root,board):
    def inner():
        global move
        root.destroy()
        move = chess.Move(st_sq, en_sq, promotion=chess.QUEEN)
        board.push(move)
        play_best_ai_move(board)
    return inner

def place_rook(st_sq, en_sq, root,board):
    def inner():
        global move
        root.destroy()
        move = chess.Move(st_sq, en_sq, promotion=chess.ROOK)
        board.push(move)
        play_best_ai_move(board)
    return inner

def place_knight(st_sq, en_sq, root,board):
    def inner():
        global move
        root.destroy()
        move = chess.Move(st_sq, en_sq, promotion=chess.KNIGHT)
        board.push(move)
        play_best_ai_move(board)
    return inner

def place_bishop(st_sq, en_sq, root,board):
    def inner():
        global move
        root.destroy()
        move = chess.Move(st_sq, en_sq, promotion=chess.BISHOP)
        board.push(move)
        play_best_ai_move(board)
    return inner

def promote_pawn(st_sq,en_sq,board):
    message_root = tk.Tk()
    message_root.geometry("400x400")
    message_root.config(bg="khaki")
    messag = tk.Label(text="What kind of peices do you want?", bg="khaki", font=("Comic Sans MS", 18),fg="#0000FF")
    messag.place(x=10, y=10)
    queen_button = tk.Button(bg="khaki", fg="#0000FF", text="Queen", font=("Comic Sans MS", 18), width=25,command=place_queen(st_sq,en_sq,message_root,board))
    queen_button.place(x=10, y=50)
    rook_button = tk.Button(bg="khaki", fg="#0000FF", text="Rook", font=("Comic Sans MS", 18), width=25,command=place_rook(st_sq,en_sq,message_root,board))
    rook_button.place(x=10, y=125)
    knight_button = tk.Button(bg="khaki", fg="#0000FF", text="Knight", font=("Comic Sans MS", 18), width=25,command=place_knight(st_sq,en_sq,message_root,board))
    knight_button.place(x=10, y=200)
    bishop_button = tk.Button(bg="khaki", fg="#0000FF", text="Bishop", font=("Comic Sans MS", 18), width=25,command=place_bishop(st_sq,en_sq,message_root,board))
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
            value = piece_pos_val[piece.piece_type][7 - chess.square_rank(square)][chess.square_file(square)]
            if piece.color == chess.BLACK:
                s_val += value
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
    W_shield_1 = 1.0
    W_shield_2 = 0.5
    W_shield_3 = 0.25
    W_open_file = -15
    W_attack_weight = {chess.QUEEN: -20, chess.ROOK: -15, chess.BISHOP: -10, chess.KNIGHT: -8, chess.PAWN: -5}
    W_central_penalty = -30
    W_escape_square = 5  
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        king_square = board.king(color)
        file = chess.square_file(king_square)
        rank = chess.square_rank(king_square)
        P1 = P2 = P3 = 0
        for i in [-2, -1, 0, 1, 2]:  
            file_to_check = file + i
            if 0 <= file_to_check < 8:  
                for j, weight in zip([1, 2, 3], [W_shield_1, W_shield_2, W_shield_3]):
                    rank_to_check = rank - j if color == chess.WHITE else rank + j
                    if 0 <= rank_to_check < 8:  
                        sq = chess.square(file_to_check, rank_to_check)
                        piece = board.piece_at(sq)
                        if piece and piece.piece_type == chess.PAWN and piece.color == color:
                            if j == 1:
                                P1 += 1
                            elif j == 2:
                                P2 += 1
                            elif j == 3:
                                P3 += 1
        pawn_shield_score = (P1 * W_shield_1) + (P2 * W_shield_2) + (P3 * W_shield_3)
        open_file_penalty = 0
        for i in [-1, 0, 1]:
            file_to_check = file + i
            if 0 <= file_to_check < 8:
                if all(board.piece_at(chess.square(file_to_check, r)) is None for r in range(8)):  
                    open_file_penalty += W_open_file
        attacking_penalty = 0
        king_zone = {king_square}
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= file + i < 8 and 0 <= rank + j < 8:
                    king_zone.add(chess.square(file + i, rank + j))
        for sq in king_zone:
            for piece_type, weight in W_attack_weight.items():
                if board.is_attacked_by(not color, sq):
                    attacking_penalty += weight
        central_penalty = W_central_penalty if board.fullmove_number < 30 and king_square in {chess.D4, chess.D5, chess.E4, chess.E5} else 0
        escape_bonus = len(list(board.legal_moves)) * W_escape_square
        king_safety_score = (pawn_shield_score + open_file_penalty + attacking_penalty + central_penalty + escape_bonus)
        if color == chess.WHITE:
            score += king_safety_score
        else:
            score -= king_safety_score
    return score

def play_best_ai_move(board):
    
    best_move = None
    best_score = float('inf') 

    for move in board.legal_moves:
        board.push(move)
        score = piece_values_checker(board)+piece_position_value(board)+center_control(board)
        +evaluate_king_safety(board)+0.1*evaluate_black_targeted_squares(board)
        +0.2*evaluate_forks(board)
        board.pop()

        if score < best_score:
            best_score = score
            best_move = move

    if best_move:
        board.push(best_move)
        
def play_again(root):
    def inner():
        root.destroy()
        main()
    return inner

def main():
    pg.init()
    screen = pg.display.set_mode((640, 640))
    pg.display.set_caption("Chess")
    pg.mixer.music.load(r"voc\war_horn_3.mp3")
    screen.blit(pg.image.load(r"pic\welcome_page.png"), (0, 0))
    pg.display.update()
    pg.mixer.music.play()
    time.sleep(2)
    board = chess.Board()
    running = True
    counter = 0
    c_m_f = False
    while running:
        for event in pg.event.get():
            if board.is_checkmate():
                color = 'black' if board.turn==chess.BLACK else 'white'
                for i in range(8):
                    for j in range(8):
                        piece = board.piece_at(chess.square(i, 7 - j))
                        if piece and piece.piece_type == chess.KING and piece.color == board.turn:
                            screen.blit(pg.image.load(r"pic\check_block.png"),(i*80,j*80))
                            pg.mixer.music.load(r"voc\مات.mp3")
                            pg.display.update()
                            pg.mixer.music.play()
                            time.sleep(2)
                pg.display.set_caption('checkmate')
                clip = moviepy.editor.VideoFileClip('checkmate.mp4')
                clip.preview()
                pg.quit()
                screen = pg.display.set_mode((640, 640))
                pg.display.set_caption('Game Over!')
                screen.blit(pg.image.load(rf"pic\{color}_lost.png"),(0,0))
                pg.display.update()
                time.sleep(1)
                root = tk.Tk()
                root.title('Play agian?')
                root.eval('tk::PlaceWindow . center')
                root.geometry('500x100')
                message = tk.Label(root, text='Game Over!Do you want to play again?', font = ("Comic Sans MS", 18))
                message.place(x=30, y=0)
                no_button = tk.Button(root, text='No', font = ("Comic Sans MS", 18),command=root.destroy)
                no_button.place(x=100, y=50 )
                yes_button = tk.Button(root, text='Yes', font = ("Comic Sans MS", 18), command=play_again(root))
                yes_button.place(x=300, y=50)
                root.mainloop()
                running = False
            elif board.is_check() and not c_m_f:
                color = 'black' if board.turn==chess.BLACK else 'white'
                screen.blit(pg.image.load(rf"pic\{color}_king_is_in_check.png"),(0,0))
                pg.mixer.music.load(r"voc\کیش.mp3")
                pg.display.update()
                pg.mixer.music.play()
                time.sleep(2)
                c_m_f = True
            elif board.is_stalemate():
                screen.blit(pg.image.load(rf"pic\stalemate.png"), (0, 0))
                pg.display.update()
                time.sleep(1)
                running = False
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if counter%2 == 0:
                    x_s, y_s = pg.mouse.get_pos()
                    piece = board.piece_at(chess.square(x_s // 80, 7 - (y_s // 80)))
                    if piece and piece.color==board.turn:
                        counter = counter+1
                    else:
                        continue
                else:
                    x_e, y_e = pg.mouse.get_pos()
                    counter = counter+1
                    if counter>=2:                
                        start_square = chess.square(x_s // 80, 7 - (y_s // 80))
                        end_square = chess.square(x_e // 80, 7 - (y_e // 80))
                        s_piece = board.piece_at(start_square)
                        try:
                            move = board.find_move(start_square,end_square)
                        except:
                            continue
                        if s_piece and move in board.legal_moves and s_piece.piece_type == chess.PAWN and (end_square // 8 == 0 or end_square // 8 == 7):
                            promote_pawn(start_square,end_square,board)
                        if move in board.legal_moves:
                            r_piece = board.piece_at(end_square)
                            board.push(move)
                            if r_piece:
                                pg.mixer.music.load(r"voc\حذف مهره.mp3")
                                pg.mixer.music.play()
                            else:
                                pg.mixer.music.load(r"voc\گذاشتن مهره.mp3")
                                pg.mixer.music.play()
                            c_m_f = False
                            play_best_ai_move(board)
        draw_board(screen)
        draw_pieces(board,screen)
        pg.display.flip()
    pg.quit()
    
if __name__ == "__main__":
    main()
