import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(x, 300))
        self.speed = 6

    def update(self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.kill()