import pygame


class BlackPiece(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"D:\PycharmProjects\CodeLearning\pygame\gobang\images\blackpiece.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position


class WhitePiece(pygame.sprite.Sprite):

    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r"D:\PycharmProjects\CodeLearning\pygame\gobang\images\whitepiece.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
