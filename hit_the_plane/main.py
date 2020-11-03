import sys
import pygame
import traceback
from pygame.locals import *
from random import *
import myplane
import enemy
import bullet
import supply

pygame.init()
pygame.mixer.init()

bg_size = width, height = 550, 600
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("plane game")

background = pygame.image.load(r"images\background.jpg").convert()

# import music
pygame.mixer.music.load(r"sounds\background_music.ogg")
pygame.mixer.music.set_volume(0.2)
bomb_sound = pygame.mixer.Sound(r"sounds\bomb.wav")
bomb_sound.set_volume(0.4)
bullet_sound = pygame.mixer.Sound(r"sounds\bullet.wav")
bullet_sound.set_volume(0.4)
get_supply_sound = pygame.mixer.Sound(r"sounds\get_supply.wav")
get_supply_sound.set_volume(0.4)
show_supply_sound = pygame.mixer.Sound(r"sounds\show_supply.wav")
show_supply_sound.set_volume(0.4)
enemy3_show_sound = pygame.mixer.Sound(r"sounds\enemy3_show.wav")
enemy3_show_sound.set_volume(0.4)
enemy1_down_sound = pygame.mixer.Sound(r"sounds\enemy1_down.wav")
enemy1_down_sound.set_volume(0.4)
enemy2_down_sound = pygame.mixer.Sound(r"sounds\enemy2_down.wav")
enemy2_down_sound.set_volume(0.4)
enemy3_down_sound = pygame.mixer.Sound(r"sounds\enemy2_down.wav")
enemy3_down_sound.set_volume(0.4)
me_down_sound = pygame.mixer.Sound(r"sounds\me_dead.wav")
me_down_sound.set_volume(0.4)
upgrade_sound = pygame.mixer.Sound(r"sounds\upgrade.wav")
upgrade_sound.set_volume(0.4)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_normal_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.NormalEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_strong_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.StrongEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_speed(target, inc):
    for each in target:
        each.speed += inc



def main():

    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    running = True

    frames = 60
    delay = 100

    # define lives
    life_image = pygame.image.load("images\life.png").convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 1
    life_display_width = life_rect.width + 5

    """define the score"""
    # load font
    score = 0
    score_font = pygame.font.Font("eng_font.ttf", 20)
    final_score_font = pygame.font.Font("eng_font.ttf", 40)
    break_record_font = pygame.font.Font("eng_font.ttf", 40)
    function_font = pygame.font.Font("eng_font.ttf", 30)
    function_pressed_font = pygame.font.Font("eng_font.ttf", 20)

    # create font surfaces
    final_score_text1 = final_score_font.render("Score", True, WHITE)
    #final score text2 is related to the game, defined in the end
    restart_text = function_font.render("RESTART", True, WHITE)
    restart_pressed_text = function_pressed_font.render("RESTART", True, WHITE)
    exit_text = function_font.render("EXIT", True, WHITE)
    exit_pressed_text = function_pressed_font.render("EXIT", True, WHITE)

    # acquire font rect
    restart_text_rect = restart_text.get_rect()
    restart_text_rect.center = (width // 2, 380)
    restart_pressed_text_rect = restart_pressed_text.get_rect()
    restart_pressed_text_rect.center = (width // 2, 380)
    exit_text_rect = exit_text.get_rect()
    exit_text_rect.center = (width // 2, 460)
    exit_pressed_text_rect = exit_pressed_text.get_rect()
    exit_pressed_text_rect.center = (width // 2, 460)

    # define levels upon scores
    level = 1
    level_font = pygame.font.Font("eng_font.ttf", 10)

    # define supply
    bomb_supply = supply.Bomb_Supply(bg_size)
    bullet_supply = supply.Bullet_Supply(bg_size)
    SUPPLY_TIME = USEREVENT
    supply_interval = 3 * 1000
    pygame.time.set_timer(SUPPLY_TIME, supply_interval)
    bomb_num = 0

    # define bomb stock
    bomb_stock1 = pygame.image.load(
        r"images\bomb.png").convert_alpha()
    bomb_stock2 = pygame.image.load(
        r"images\bomb.png").convert_alpha()
    bomb_stock3 = pygame.image.load(
        r"images\bomb.png").convert_alpha()
    bomb_stocks = [bomb_stock1, bomb_stock2, bomb_stock3]
    bomb_stock_rect = bomb_stock1.get_rect()
    bomb_stock_display_width = bomb_stock_rect.width + 5

    # newborn timer
    NEWBORN_TIMER = USEREVENT + 2

    # super bullet timer
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # super bullet signal
    is_double_bullet = False

    # bomb confirm switch
    bomb_confirm = False

    # switch of record when game over
    end_recorded = False

    # define pause and continue button
    paused = False
    pause_nor_image = pygame.image.load(
        "images\pause1.png").convert_alpha()
    pause_pressed_image = pygame.image.load(
        "images\pause2.png").convert_alpha()
    continue_nor_image = pygame.image.load(
        "images\continue1.png").convert_alpha()
    continue_pressed_image = pygame.image.load(
        "images\continue2.png").convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.right, paused_rect.top = width - 10, 10
    pause_image = pause_nor_image

    # define game over buttons
    restart_pressed = False
    exit_pressed = False

    # creating my plane
    me = myplane.MyPlane(bg_size)
    me_down_index = 0

    # creating the enemy planes
    enemies = pygame.sprite.Group()

    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)
    e1_destroy_index = 0

    normal_enemies = pygame.sprite.Group()
    add_normal_enemies(normal_enemies, enemies, 5)
    e2_destroy_index = 0
    e2_hit = False

    strong_enemies = pygame.sprite.Group()
    add_strong_enemies(strong_enemies, enemies, 1)
    e3_destroy_index = 0
    e3_hit = False

    # creating bullets
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4  # customized, to ensure the number of bullets is adequate
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8  # customized, to ensure the number of bullets is adequate
    for i in range(BULLET1_NUM):
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if life_num:
                """detection of regular game page and pause page """
                # operation of pause and continue
                if event.type == MOUSEBUTTONDOWN and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, supply_interval)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

                elif event.type == MOUSEMOTION:
                    if paused_rect.collidepoint(event.pos):
                        if paused:
                            pause_image = continue_pressed_image
                        else:
                            pause_image = pause_pressed_image
                    else:
                        if paused:
                            pause_image = continue_nor_image
                        else:
                            pause_image = pause_nor_image

                elif event.type == MOUSEBUTTONUP:
                    if paused_rect.collidepoint(event.pos):
                        if paused:
                            pause_image = continue_nor_image
                        else:
                            pause_image = pause_nor_image


                # trigger of supply
                elif event.type == SUPPLY_TIME:
                    show_supply_sound.play()
                    if choice((True, False)):
                        bomb_supply.reset()
                    else:
                        bullet_supply.reset()

                # detect the end of bullet supply
                elif event.type == DOUBLE_BULLET_TIME:
                    is_double_bullet = False
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

                # bomb bomb
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if bomb_num > 0:
                            bomb_sound.play()
                            bomb_num -= 1
                            bomb_confirm = True

                # out of newborn
                elif event.type == NEWBORN_TIMER:
                    me.newborn = False
                    pygame.time.set_timer(NEWBORN_TIMER, 0)

            """detection of game over page"""
            if life_num == 0:
                if event.type == MOUSEMOTION:
                    if restart_text_rect.collidepoint(event.pos):
                        restart_pressed = True
                    elif exit_text_rect.collidepoint(event.pos):
                        exit_pressed = True
                    else:
                        restart_pressed = False
                        exit_pressed = False

                elif event.type == MOUSEBUTTONDOWN:
                    if restart_text_rect.collidepoint(event.pos):
                        life_num = 3
                        bomb_num = 0
                        score = 0
                        delay = 100
                        is_double_bullet = False
                        paused = False
                        restart_pressed = False
                        end_recorded = False
                        pygame.mixer.music.play(-1)
                        pygame.time.set_timer(SUPPLY_TIME, supply_interval)

                        level = 1   #need to reset enemies

                        #reset enemies
                        enemies.empty()

                        small_enemies.empty()
                        add_small_enemies(small_enemies, enemies, 15)
                        e1_destroy_index = 0

                        normal_enemies.empty()
                        add_normal_enemies(normal_enemies, enemies, 5)
                        e2_destroy_index = 0
                        e2_hit = False

                        strong_enemies.empty()
                        add_strong_enemies(strong_enemies, enemies, 1)
                        e3_destroy_index = 0
                        e3_hit = False

                    elif exit_text_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        screen.blit(background, (0, 0))

        # level adjustment
        if level == 1 and score >= 50000:
            level = 2
            upgrade_sound.play()
            # add 3 small enemies, 2 normal enemy and 1 strong enemy
            add_small_enemies(small_enemies, enemies, 3)
            add_normal_enemies(normal_enemies, enemies, 2)
            add_strong_enemies(strong_enemies, enemies, 1)
            # increase the speed of small enemy
            add_speed(small_enemies, 1)

        if level == 2 and score >= 120000:
            level = 3
            upgrade_sound.play()
            # add 5 small enemies, 3 normal enemy and 2 strong enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_normal_enemies(normal_enemies, enemies, 3)
            add_strong_enemies(strong_enemies, enemies, 2)
            # increase the speed of small enemy
            add_speed(small_enemies, 1)
            add_speed(normal_enemies, 1)

        if level == 3 and score >= 200000:
            level = 4
            upgrade_sound.play()
            # add 5 small enemies, 3 normal enemy and 2 strong enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_normal_enemies(normal_enemies, enemies, 3)
            add_strong_enemies(strong_enemies, enemies, 2)
            # increase the speed of small enemy
            add_speed(small_enemies, 1)
            add_speed(normal_enemies, 1)

        elif level == 4 and score >= 300000:
            level = 5
            upgrade_sound.play()
            # add 5 small enemies, 3 normal enemy and 2 strong enemy
            add_small_enemies(small_enemies, enemies, 5)
            add_normal_enemies(normal_enemies, enemies, 3)
            add_strong_enemies(strong_enemies, enemies, 2)
            # increase the speed of small enemy
            add_speed(small_enemies, 1)
            add_speed(normal_enemies, 1)

        if life_num and not paused:
            # detecting user's keyboard
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # depicting bullets
            if not (delay % 10):
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx + 30, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx - 33, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # depicting bullets
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_down = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    for e in enemies_down:
                        if e in normal_enemies or e in strong_enemies:
                            e.hp -= 1
                            e.hit = True
                            if e.hp == 0:
                                e.active = False
                        else:
                            e.active = False
                        b.active = False

            # depicting enemy planes
            for each in strong_enemies:
                if each.active:
                    if bomb_confirm:
                        if each.rect.bottom > -10:
                            each.active = False
                    else:
                        each.move()
                        # play sound before showing
                        if 0 > each.rect.bottom > -50:
                            enemy3_show_sound.play()

                        # draw hp bar
                        pygame.draw.line(screen, BLACK, \
                                         (each.rect.left, each.rect.top - 5), \
                                         (each.rect.right, each.rect.top - 5), \
                                         2)
                        hp_remain = each.hp / enemy.StrongEnemy.hp
                        hp_color = GREEN if hp_remain > 0.2 else RED
                        pygame.draw.line(screen, hp_color, \
                                         (each.rect.left, each.rect.top - 5), \
                                         (each.rect.width * hp_remain + each.rect.left, \
                                          each.rect.top - 5), \
                                         2)
                        if each.hit:
                            screen.blit(each.hit_image, each.rect)
                            each.hit = False
                        else:
                            screen.blit(each.image, each.rect)
                else:
                    # conduct destroy
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % each.destroy_steps
                        if e3_destroy_index == 0:
                            score += 15000
                            each.reset()

            for each in normal_enemies:
                if each.active:
                    if bomb_confirm:
                        if each.rect.bottom > -10:
                            each.active = False
                    else:
                        each.move()

                        # draw hp bar
                        pygame.draw.line(screen, BLACK, \
                                         (each.rect.left, each.rect.top - 5), \
                                         (each.rect.right, each.rect.top - 5), \
                                         2)
                        hp_remain = each.hp / enemy.NormalEnemy.hp
                        hp_color = GREEN if hp_remain > 0.2 else RED
                        pygame.draw.line(screen, hp_color, \
                                         (each.rect.left, each.rect.top - 5), \
                                         (each.rect.width * hp_remain + each.rect.left, \
                                          each.rect.top - 5), \
                                         2)
                        if each.hit:
                            screen.blit(each.hit_image, each.rect)
                            each.hit = False
                        else:
                            screen.blit(each.image, each.rect)
                else:
                    # conduct destroy
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % each.destroy_steps
                        if e2_destroy_index == 0:
                            score += 5000
                            each.reset()

            for each in small_enemies:
                if each.active:
                    if bomb_confirm:
                        if each.rect.bottom > -10:
                            each.active = False
                    else:
                        each.move()
                        screen.blit(each.image, each.rect)
                else:
                    # conduct destroy
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % each.destroy_steps
                        if e1_destroy_index == 0:
                            score += 500
                            each.reset()

            # detect collision of our plane
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.newborn:
                me.active = False
                for e in enemies_down:
                    e.active = False

            # depicting my plane
            if me.active:
                if not me.newborn:
                    me.switchShape()
                    screen.blit(me.images[me.order], me.rect)
                else:
                    # blink when new born
                    newborn_countdown -= 1
                    if not (newborn_countdown % (frames // 7)):
                        screen.blit(me.images[me.order], me.rect)
            else:
                # conduct destroy
                me_down_sound.play()
                if not (delay % 3):
                    screen.blit(me.destroy_images[me_down_index], me.rect)
                    me_down_index = (me_down_index + 1) % me.destroy_steps
                    if me_down_index == 0:
                        if life_num:
                            life_num -= 1
                            me.reset()
                            newborn_countdown = frames * 2
                            pygame.time.set_timer(NEWBORN_TIMER, 2 * 1000)

            # depicting supply
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_supply_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_supply_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18 * 1000)
                    bullet_supply.active = False

            # depict bomb stock
            for i in range(bomb_num):
                screen.blit(bomb_stocks[i], \
                            (20 + bomb_stock_display_width * i, \
                             height - bomb_stock_rect.height - 20))

            # depict life stock
            for i in range(life_num):
                screen.blit(life_image, \
                            (width - 20 - life_display_width * (1 + i), \
                             height - life_rect.height - 20))

            if delay:
                delay -= 1
            else:
                delay = 100

        elif life_num == 0:
            if not end_recorded:
                # game over
                end_recorded = True

                # stop music and sound
                pygame.mixer.music.stop()
                pygame.mixer.stop()

                # stop supply system
                pygame.time.set_timer(SUPPLY_TIME, 0)

                # load record
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                # store score if the best
                if score > record_score:
                    break_record = True
                    record_score = score
                    with open("record.txt", "w") as f:
                        f.write(str(score))

                else:
                    break_record = False

            """depict the screen of end of the game"""
            #record score display
            record_score_text = score_font.render("Best score:{}".format(record_score), True, WHITE)
            screen.blit(record_score_text, (10, 5))

            #break record display
            if break_record:
                break_record_text = break_record_font.render("BREAK RECORD", True, WHITE)
                screen.blit(break_record_text, (width // 2 - break_record_text.get_width() // 2, 100 - 30))

            # score display
            #final score text1 is solid, defined in the beginning
            screen.blit(final_score_text1, (width // 2 - final_score_text1.get_width() // 2, 190 - 30))
            final_score_text2 = final_score_font.render("{}".format(score), True, WHITE)
            screen.blit(final_score_text2, (width // 2 - final_score_text2.get_width() // 2, 270 - 30))

            #display of restart and exit
            if restart_pressed:
                screen.blit(restart_pressed_text, (width // 2 - restart_pressed_text_rect.width//2, 380))
            else:
                screen.blit(restart_text, (width // 2 - restart_text_rect.width//2, 380))
            if exit_pressed:
                screen.blit(exit_pressed_text, (width // 2 - exit_pressed_text_rect.width // 2, 460))
            else:
                screen.blit(exit_text, (width // 2 - exit_text_rect.width // 2, 460))

        if life_num:
            """only print if pause or in game"""

            # print the score
            score_text = score_font.render("Score : {}".format(score), True, WHITE)
            screen.blit(score_text, (10, 5))

            # print the level
            level_text = level_font.render("Level : {}".format(level), True, WHITE)
            screen.blit(level_text, (50, 30))

            screen.blit(pause_image, paused_rect)

        pygame.display.flip()

        clock.tick(frames)

        if bomb_confirm:
            # bomb used
            bomb_confirm = False


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
