import pygame
import math

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, obstacle_type):
        super().__init__()

        self.obstacle_type = obstacle_type

        if obstacle_type == "small":
            self.image = pygame.Surface((20, 30))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(midbottom=(x, 400))

        elif obstacle_type == "tall":
            self.image = pygame.image.load("assets/sprites/CactoTall.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 1.3), int(self.image.get_height() * 1.3)))
            self.rect = self.image.get_rect(midbottom=(x, 400))

        elif obstacle_type == "flying":
            self.image = pygame.Surface((30, 20))
            self.image.fill((0, 200, 255))
            self.rect = self.image.get_rect(midbottom=(x, 320))

        self.base_y = self.rect.y
        self.timer = 0

    def update(self, speed):
        self.rect.x -= speed

        if self.obstacle_type == "flying":
            self.timer += 0.1
            self.rect.y = self.base_y + int(math.sin(self.timer) * 45)

        if self.rect.right < 0:
            self.kill()