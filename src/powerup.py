import pygame
import math

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, power_type):
        super().__init__()
        self.type = power_type
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        if self.type == "shield":
            pygame.draw.circle(self.image, (139, 233, 253), (15, 15), 15)
            pygame.draw.circle(self.image, (255, 255, 255), (15, 15), 15, 2)
        elif self.type == "multiplier":
            pygame.draw.polygon(self.image, (241, 250, 140), [(15, 0), (30, 15), (15, 30), (0, 15)])

        self.rect = self.image.get_rect(midbottom=(x, 340))
        self.base_y = self.rect.y
        self.timer = 0

    def update(self, speed) -> None:
        self.rect.x -= speed

        self.timer += 0.1
        self.rect.y = self.base_y + int(math.sin(self.timer) * 5)

        if self.rect.right < 0:
            self.kill()
