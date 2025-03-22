import chess
import pygame as pg
import time
import moviepy.editor

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
                            pg.display.update()
                            time.sleep(1)
                screen.blit(pg.image.load(rf"pic\{color}_lost.png"),(0,0))
                pg.display.update()
                time.sleep(1)
                running = False
            elif board.is_check() and not c_m_f:
                color = 'black' if board.turn==chess.BLACK else 'white'
                screen.blit(pg.image.load(rf"pic\{color}_king_is_in_check.png"),(0,0))
                pg.mixer.music.load(r"voc\کیش.mp3")
                pg.display.update()
                pg.mixer.music.play()
                time.sleep(1)
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
                    if piece:
                        counter = counter+1
                else:
                    x_e, y_e = pg.mouse.get_pos()
                    counter = counter+1
                    if counter>=2:                
                        start_square = chess.square(x_s // 80, 7 - (y_s // 80))
                        end_square = chess.square(x_e // 80, 7 - (y_e // 80))
                        move = board.find_move(start_square,end_square)
                        if move in board.legal_moves:
                            piece = board.piece_at(end_square)
                            board.push(move)
                            if piece:
                                pg.mixer.music.load(r"voc\حذف مهره.mp3")
                                pg.mixer.music.play()
                            else:
                                pg.mixer.music.load(r"voc\گذاشتن مهره.mp3")
                                pg.mixer.music.play()
                            c_m_f = False
        draw_board(screen)
        draw_pieces(board,screen)
        pg.display.flip()
    pg.quit()
    
if __name__ == "__main__":
    main()