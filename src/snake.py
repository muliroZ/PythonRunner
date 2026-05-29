import pygame

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(midbottom=(100, 400))

        self.velocity_y = 0
        self.gravity = 1
        self.jump_strength = -15

    def update(self):
        self.apply_gravity()

    def jump(self):
        if self.rect.bottom >= 400:
            self.velocity_y = self.jump_strength

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom >= 400:
            self.rect.bottom = 400