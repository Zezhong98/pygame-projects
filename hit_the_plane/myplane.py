import pygame

class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        image1 = pygame.image.load(
            "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\me1.png").convert_alpha()
        image2 = pygame.image.load(
            "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\me2.png").convert_alpha()
        self.images = (image1, image2)
        self.destroy_images = []
        self.destroy_images.extend([ \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\me_down1.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\me_down2.png").convert_alpha(), \
            pygame.image.load(
                "D:\PycharmProjects\CodeLearning\pygame\hit_the_plane\images\me_down3.png").convert_alpha()
            ])
        self.destroy_steps = len(self.destroy_images)
        self.order = 0
        self.delay = 100
        self.rect = image1.get_rect()
        self.down_distance = 10
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height-self.rect.height - self.down_distance
        self.speed = 10
        self.active = True
        self.mask = pygame.mask.from_surface(self.images[0])
        self.newborn = False

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - self.down_distance:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - self.down_distance

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def switchShape(self):
        self.delay-=1
        if self.delay == 0:
            self.delay = 100
        if not self.delay % 5:
            self.order = (self.order+1)%2

    def reset(self):
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2, \
            self.height - self.rect.height - self.down_distance
        self.active = True
        self.newborn = True














