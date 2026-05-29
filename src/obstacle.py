import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, obstacle_type):
        super().__init__()

        if obstacle_type == "small":
            self.image = pygame.Surface((20, 30))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(midbottom=(x, 400))
        elif obstacle_type == "tall":
            self.image = pygame.Surface((20, 60))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(midbottom=(x, 400))
        elif obstacle_type == "flying":
            self.image = pygame.Surface((30, 20))
            self.image.fill((0, 200, 255))
            self.rect = self.image.get_rect(midbottom=(x, 340))

    def update(self, speed):
        self.rect.x -= speed

        if self.rect.right < 0:
            self.kill()