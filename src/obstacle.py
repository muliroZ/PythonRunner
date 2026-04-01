import pygame
import random

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, obstacle_type):
        super().__init__()

        obstacle_type = random.choice(["small", "tall"])

        if obstacle_type == "small":
            self.image = pygame.Surface((20, 30))
        else:
            self.image = pygame.Surface((20, 60))

        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midbottom=(x, 300))

    def update(self, speed):
        self.rect.x -= speed

        if self.rect.right < 0:
            self.kill()