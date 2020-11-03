import pygame
import sys
import traceback
import math
from pygame.locals import *
from random import *

BALL_SIZE = 100
MAX_SPEED = 5

class Ball(pygame.sprite.Sprite):
    def __init__(self, image, static_image, position, speed, bg_size, target_frequency):
        pygame.sprite.Sprite.__init__(self)

        static_image = pygame.image.load(static_image).convert_alpha()
        static_rect = static_image.get_bounding_rect(min_alpha=1)
        self.static_image = static_image.subsurface(static_rect).copy()
        self.static_image = pygame.transform.smoothscale(self.static_image, (BALL_SIZE, BALL_SIZE))

        image = pygame.image.load(image).convert_alpha()
        rect = image.get_bounding_rect(min_alpha=1)
        self.image = image.subsurface(rect).copy()
        self.image = pygame.transform.smoothscale(self.image, (BALL_SIZE, BALL_SIZE))

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.direction = [choice([-1,1]),choice([-1,1])]
        self.speed = speed
        self.width, self.height = bg_size
        self.radius = BALL_SIZE//2
        self.target = target_frequency
        self.control = False
        self.bounce = False

    def move(self):
        if not self.control:
            shift = (self.speed[0]*self.direction[0], self.speed[1]*self.direction[1])
        else:
            shift = (self.speed[0], self.speed[1])
        self.rect = self.rect.move(shift)
        if self.rect.left<=0 or self.rect.right>=self.width:
            if self.control:
                self.speed[0] *= -1
            else:
                self.direction[0]*=-1
        if self.rect.top<=0 or self.rect.bottom>=self.height:
            if self.control:
                self.speed[1] *= -1
            else:
                self.direction[1] *= -1

    def check(self, motion):
        if self.target < motion < self.target+5:
            return True
        else:
            return False

class Mark(pygame.sprite.Sprite):
    def __init__(self, image, bg_size, mark_size):
        pygame.sprite.Sprite.__init__(self)

        self.mark = pygame.image.load(image).convert_alpha()
        self.mark_rect = self.mark.get_rect()
        # self.mark_rect.inflate_ip(1500,1000)
        self.mark_rect.left, self.mark_rect.top = \
            (bg_size[0]-self.mark_rect.width)//2,\
            (bg_size[1]-self.mark_rect.height)//2

        self.mouse = pygame.image.load("D:\PycharmProjects\CodeLearning\pygame\play_the_ball\mouse.png")
        self.mouse_rect = self.mouse.get_rect()
        pygame.mouse.set_visible(False)
        self.mouse_rect.left, self.mouse_rect.top = self.mark_rect.left, self.mark_rect.top


def collision_check(item, targets):
    for target in targets:
        distance = math.sqrt(math.pow(item.rect.center[0]-target.rect.center[0],2)+
                             math.pow(item.rect.center[1]-target.rect.center[1],2))
        if distance<=(item.rect.width+target.rect.width)//2:
            return True
    return False

def main():

    #initialization
    pygame.init()
    pygame.mixer.init()

    #files of images and sounds
    ball_image = "Poke_ball.png"
    bg_image = "Pokemon.jpg"
    static_ball_image = "Poke_ball_green.png"
    mark_image = r"D:\PycharmProjects\CodeLearning\pygame\play_the_ball\robrob.png"
    background_music = 'D:\PycharmProjects\CodeLearning\pygame\play_the_ball\Memories.ogg'
    fart_sound = r"D:\PycharmProjects\CodeLearning\pygame\play_the_ball\fart.wav"
    win_sound = r"D:\PycharmProjects\CodeLearning\pygame\play_the_ball\clap.wav"
    lose_sound = r"D:\PycharmProjects\CodeLearning\pygame\play_the_ball\loser.wav"

    #main state
    running = True

    #setting window
    screen_size = width, height = 1000,600
    screen_color = (255,255,255)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("play the ball")

    #creating balls group
    ball_group = pygame.sprite.Group()
    BALL_NUM = 5

    #creating holes group
    holes = []


    background = pygame.image.load(bg_image).convert()

    mark = Mark(mark_image, screen_size, (200,100))

    clock = pygame.time.Clock()

    #recorder of mouse frequency
    motion = 0

    #play background music
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.4)

    #game over when music ends
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    #event of per second
    CHECKTARGET = USEREVENT+1
    pygame.time.set_timer(CHECKTARGET, 1000)

    #special sounds
    fart_sound = pygame.mixer.Sound(fart_sound)
    fart_sound.set_volume(0.5)
    win_sound = pygame.mixer.Sound(win_sound)
    lose_sound = pygame.mixer.Sound(lose_sound)

    # key repeating
    pygame.key.set_repeat(100, 100)

    # initializing balls
    for i in range(BALL_NUM):
        position = randint(0, width-BALL_SIZE), randint(0,height-BALL_SIZE)
        speed = [randint(1,MAX_SPEED), randint(1,MAX_SPEED)]
        ball = Ball(ball_image, static_ball_image, position, speed, (width, height), 5*(i+1))
        while pygame.sprite.spritecollide(ball, ball_group, False, pygame.sprite.collide_circle):
            ball.rect.left, ball.rect.top = randint(0, width-BALL_SIZE), randint(0,width-BALL_SIZE)
        ball_group.add(ball)

    hole_width, hole_height = int(ball.rect.width*1.05), int(ball.rect.height*1.05)
    for i in range(BALL_NUM):
        position_horizontal, position_vertical = randint(hole_width, width - hole_width), randint(hole_height, height - hole_height)
        holes.append([position_horizontal, position_vertical])


    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == GAMEOVER:
                lose_sound.play()
                pygame.time.delay(5000)
                running = False

            if event.type == CHECKTARGET:
                if motion:
                    for ball in ball_group:
                        if ball.check(motion):
                            ball.control = True
                            ball.speed[0] = ball.speed[0]*ball.direction[0]
                            ball.speed[1] = ball.speed[1]*ball.direction[1]
                    motion = 0
            if event.type == MOUSEMOTION:
                motion+=1

            if event.type == KEYDOWN:
                if event.key == K_w:
                    for ball in ball_group:
                        if ball.control:
                            ball.speed[1] -= 1
                if event.key == K_s:
                    for ball in ball_group:
                        if ball.control:
                            ball.speed[1] += 1
                if event.key == K_a:
                    for ball in ball_group:
                        if ball.control:
                            ball.speed[0] -= 1
                if event.key == K_d:
                    for ball in ball_group:
                        if ball.control:
                            ball.speed[0] += 1

        screen.fill(screen_color)
        screen.blit(background, (0,0))
        screen.blit(mark.mark, mark.mark_rect)

        for center in holes:
            pygame.draw.circle(screen, [0,0,0], center, max(hole_width, hole_height)//2, 5)

        mark.mouse_rect.left, mark.mouse_rect.top = pygame.mouse.get_pos()
        if mark.mouse_rect.left < mark.mark_rect.left:
            mark.mouse_rect.left = mark.mark_rect.left
        elif mark.mouse_rect.right > mark.mark_rect.right:
            mark.mouse_rect.right = mark.mark_rect.right
        if mark.mouse_rect.top < mark.mark_rect.top:
            mark.mouse_rect.top = mark.mark_rect.top
        elif mark.mouse_rect.bottom > mark.mark_rect.bottom:
            mark.mouse_rect.bottom = mark.mark_rect.bottom
        screen.blit(mark.mouse, mark.mouse_rect)

        for ball in ball_group:
            ball.move()
            if ball.bounce:
                ball.speed = [randint(1,MAX_SPEED), randint(1,MAX_SPEED)]
                ball.bounce = False
            if not ball.control:
                screen.blit(ball.image, ball.rect)
            else:
                screen.blit(ball.static_image, ball.rect)

            #collipse detection
            ball_group.remove(ball)
            if pygame.sprite.spritecollide(ball, ball_group, False, pygame.sprite.collide_circle):
                if not ball.control:
                    ball.direction[0] *= -1
                    ball.direction[1] *= -1
                else:
                    ball.direction = list(map(lambda x:-x//abs(x) if x else 1, ball.speed))
                    ball.speed = list(map(lambda x:abs(x), ball.speed))
                ball.bounce = True
                ball.control = False
                fart_sound.play()
            ball_group.add(ball)

            # for center in holes
            for c in holes:
                if c[0]-5<ball.rect.center[0]<c[0]+5 and c[1]-5<ball.rect.center[1]<c[1]+5:
                    win_sound.play()
                    holes.remove(c)
                    ball_group.remove(ball)

        if not ball_group:
            fart_sound.play()
            pygame.time.delay(6*1000)
            pygame.quit()

        pygame.display.flip()
        clock.tick(30)




if __name__=="__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()

