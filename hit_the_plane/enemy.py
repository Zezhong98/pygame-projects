import pygame
from random import *

INVALID_EDGE = 50

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy1_1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy1_1.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy1_2.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy1_3.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy1_4.png").convert_alpha()
            ])
        self.destroy_steps = len(self.destroy_images)
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.rect.left, self.rect.top = \
                        randint(INVALID_EDGE, self.width-self.rect.width-INVALID_EDGE), \
                        randint(-5 * self.height, 0)
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(INVALID_EDGE, self.width - self.rect.width-INVALID_EDGE), \
            randint(-5 * self.height, 0)
        self.active = True

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

class NormalEnemy(pygame.sprite.Sprite):
    hp = 8

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy2_1.png").convert_alpha()
        self.hit_image = pygame.image.load("D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy2_1.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy2_2.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy2_3.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy2_4.png").convert_alpha()
        ])
        self.destroy_steps = len(self.destroy_images)
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
                        randint(INVALID_EDGE, self.width-self.rect.width-INVALID_EDGE), \
                        randint(-10 * self.height, -self.height)
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = NormalEnemy.hp
        self.hit = False

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(INVALID_EDGE, self.width - self.rect.width-INVALID_EDGE), \
            randint(-10 * self.height, -self.height)
        self.active = True
        self.hp = NormalEnemy.hp

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

class StrongEnemy(pygame.sprite.Sprite):
    hp = 20

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy3_1.png").convert_alpha()
        self.hit_image = pygame.image.load("D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy3_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy3_1.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy3_2.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy3_3.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy3_4.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy3_5.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\enemy3_6.png").convert_alpha()
        ])
        self.destroy_steps = len(self.destroy_images)
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.top = \
                        randint(INVALID_EDGE, self.width-self.rect.width-INVALID_EDGE), \
                        randint(-15 * self.height, -5 * self.height)
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = StrongEnemy.hp
        self.hit = False

    def reset(self):
        self.rect.left, self.rect.top = \
            randint(INVALID_EDGE, self.width - self.rect.width-INVALID_EDGE), \
            randint(-10 * self.height, -self.height)
        self.active = True
        self.hp = StrongEnemy.hp

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()