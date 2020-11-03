import pygame
import sys
import random
import pieces
import user
import pieceboard
import random
import traceback

from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 1000, 652
piece_size = (35, 35)
chessboard_margin = (6, 6)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("gobang chess")

frames = 60

# load pictures
chessboard = pygame.image.load(r"images\chessboard.png").convert()
background = pygame.image.load(r"images/background.jpg").convert()
chessboard_rect = chessboard.get_rect()
dialog = pygame.image.load("images/dialog.png").convert_alpha()
dialog_rect = dialog.get_rect()

# load font files
chn_font = pygame.font.Font("font/chn.ttf", 40)
chn_bold_font = pygame.font.Font("font/chn_bold.ttf", 60)
chn_bold_font_sm = pygame.font.Font("font/chn_bold.ttf", 55)

# create font surface
restart_text = chn_bold_font.render("再来一局", True, (153, 88, 42))
restart_text_sm = chn_bold_font_sm.render("再来一局", True, (153, 88, 42))
restart_text_rect = restart_text.get_rect()
restart_text_sm_rect = restart_text_sm.get_rect()
quit_text = chn_bold_font.render("结束游戏", True, (153, 88, 42))
quit_text_sm = chn_bold_font_sm.render("结束游戏", True, (153, 88, 42))
quit_text_rect = quit_text.get_rect()
quit_text_sm_rect = quit_text_sm.get_rect()

##### sound unfinished, continue in the end
# load music
bgm_num = 8
# RESTART USE
bgm_index = random.randint(1,8)
bgm_path = "sounds/music" + str(bgm_index) + ".ogg"
pygame.mixer.music.load(bgm_path)
pygame.mixer.music.set_volume(0.3)
# RESTART USE
winning_sound = pygame.mixer.Sound("sounds/clapping.wav")
winning_sound.set_volume(0.4)
# miss sound of piece
# miss sound of beginning of the game


def main():
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    running = True
    round_end = False

    black_turn = True

    on_restart = False
    on_quit = False

    piece_board = pieceboard.PieceBoard(piece_size[0]
                                        , piece_size[1]
                                        , (width-chessboard_rect.width)//2 + chessboard_margin[0]
                                        , chessboard_margin[1])

    # define prepieces (piece shadow when mouse on the board)
    preblackpiece = pygame.image.load(
        r"D:\PycharmProjects\CodeLearning\pygame\gobang\images\blackpiece.png").convert_alpha()
    prewhitepiece = pygame.image.load(
        r"D:\PycharmProjects\CodeLearning\pygame\gobang\images\whitepiece.png").convert_alpha()
    preblackpiece.set_alpha(128)
    prewhitepiece.set_alpha(128)
    prepieceposition = (-1, -1)

    # initialize users
    flag = bool(random.randint(0, 1))
    user1 = user.User("帅气的 zzz", flag)
    user2 = user.User("lzn", not flag)

    # user name text
    user1_name_text = chn_font.render(user1.name, True, (73, 48, 107))
    user2_name_text = chn_font.render(user2.name, True, (73, 48, 107))
    user1_name_text_rect = user1_name_text.get_rect()
    user2_name_text_rect = user2_name_text.get_rect()
    user_text_top = 50
    user1_text_left = (width - chessboard_rect.w) // 20
    user2_text_left = (width - chessboard_rect.w) * 11 // 20 + chessboard_rect.w
    left_space_center = (width - chessboard_rect.w) // 2 // 2
    right_space_center = (width - chessboard_rect.w) // 4 * 3 + chessboard_rect.w
    user1_name_text_rect.top, user1_name_text_rect.centerx = user_text_top, left_space_center
    user2_name_text_rect.top, user2_name_text_rect.centerx = user_text_top, right_space_center

    # score text
    score_text = chn_bold_font_sm.render("0 : 0", True, (73, 48, 107))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (width // 2, height * 0.9)

    # color possession image
    black_color_possesion = pygame.image.load("images/blackpiece_raw.png").convert_alpha()
    white_color_possesion = pygame.image.load("images/whitepiece_raw.png").convert_alpha()
    user1_color_rect = black_color_possesion.get_rect()
    user1_color_rect.centerx, user1_color_rect.centery = width // 2 - chessboard_rect.w * 1 // 3, score_text_rect.centery
    user2_color_rect = black_color_possesion.get_rect()
    user2_color_rect.centerx, user2_color_rect.centery = width // 2 + chessboard_rect.w * 1 // 3, score_text_rect.centery

    # initialize restart and quit text position
    restart_text_rect.move_ip((width - restart_text_rect.width) // 2, height * 5 // 10)
    restart_text_sm_rect.center = restart_text_rect.center
    quit_text_rect.move_ip((width - quit_text_rect.width) // 2, height * 7 // 10)
    quit_text_sm_rect.center = quit_text_rect.center

    while running:

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if round_end:
                # detection when a round is over
                if event.type == MOUSEBUTTONDOWN:
                    temp_position = pygame.mouse.get_pos()

                    if restart_text_rect.collidepoint(*temp_position):
                        # start a new game, initialize all parameters
                        piece_board.reset()

                        round_end = False

                        black_turn = True   # wiating to be modified, for class User has not been writen

                    elif quit_text_rect.collidepoint(*temp_position):
                        pygame.quit()
                        sys.exit()

                elif event.type == MOUSEMOTION:
                    temp_position = pygame.mouse.get_pos()

                    if restart_text_rect.collidepoint(*temp_position):
                        on_restart = True

                    elif quit_text_rect.collidepoint(*temp_position):
                        on_quit = True
                    else:
                        on_restart = on_quit = False

            else:
                # detection when game is going
                if event.type == MOUSEBUTTONDOWN:
                    # click mouse button to put piece down

                    temp_position = pygame.mouse.get_pos()

                    if inChessboardCheck(temp_position):
                        # it only works when click in the chessboard

                        std_position = piece_board.getCoordinate(temp_position, black_turn)

                        if std_position[0] != -1:
                            # position has not been covered
                            # add black(white) piece to its list
                            if black_turn:
                                piece_board.blackOnBoard.append(pieces.BlackPiece(std_position))
                            else:
                                piece_board.whiteOnBoard.append(pieces.WhitePiece(std_position))

                            black_turn = not black_turn

                elif event.type == MOUSEMOTION:
                    temp_position = pygame.mouse.get_pos()

                    if inChessboardCheck(temp_position):
                        # it only works when click in the chessboard

                        std_position = piece_board.getStdPosition(temp_position)

                        if std_position[0] != -1:
                            # position has not been covered
                            # set pre position as std position
                            prepieceposition = std_position

        # draw the background and chessboard
        screen.blit(background, (0, 0))
        screen.blit(chessboard, ((width-chessboard_rect.width)//2, 0))

        # draw user info
        screen.blit(user1_name_text, user1_name_text_rect)
        screen.blit(user2_name_text, user2_name_text_rect)

        # draw the score
        screen.blit(score_text, score_text_rect)

        # draw the color possession
        if not round_end:
            if user1.black:
                screen.blit(black_color_possesion, user1_color_rect)
                screen.blit(white_color_possesion, user2_color_rect)
            else:
                screen.blit(white_color_possesion, user1_color_rect)
                screen.blit(black_color_possesion, user2_color_rect)

        # draw the pieces
        for one in piece_board.blackOnBoard:
            screen.blit(one.image, (one.rect.left, one.rect.top))
        for one in piece_board.whiteOnBoard:
            screen.blit(one.image, (one.rect.left, one.rect.top))

        if round_end:
            if on_restart:
                screen.blit(restart_text_sm, restart_text_sm_rect)
            else:
                screen.blit(restart_text, restart_text_rect)
            if on_quit:
                screen.blit(quit_text_sm, quit_text_sm_rect)
            else:
                screen.blit(quit_text, quit_text_rect)

        else:
            # draw the pre piece
            if prepieceposition[0] > -1:
                if black_turn:
                    screen.blit(preblackpiece, prepieceposition)
                else:
                    screen.blit(prewhitepiece, prepieceposition)

            if piece_board.ifOver():
                # detect if game is over after drawing
                round_end = True
                # reset user paramters
                userReset(user1, user2, black_turn)
                score_text = chn_bold_font_sm.render(str(user1.winnings) + " : " + str(user2.winnings), True,
                                                     (73, 48, 107))
                # save data into files

        pygame.display.flip()

        clock.tick(frames)


def userReset(user1, user2, black_turn):
    """
    winner count +1
    redistribute color (not draw the color during round end)
    """
    if black_turn:
        # white wins
        if user1.black:
            # user2 wins
            user2.winnings += 1
            user2.black = False
            user1.black = True
        else:
            # user1 wins
            user1.winnings += 1
            user1.black = False
            user2.black = True
    else:
        # black wins
        if user1.black:
            # user1 wins
            user1.winnings += 1
            user1.black = False
            user2.black = True
        else:
            # user2 wins
            user2.winnings += 1
            user2.black = False
            user1.black = True


def inChessboardCheck(position):
    if not (position[0] < (width - chessboard_rect.width) // 2
            or position[0] > (width + chessboard_rect.width) // 2
            or position[1] > chessboard_rect.height):
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()