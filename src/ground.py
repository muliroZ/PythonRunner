import pygame

class Ground:
    def __init__(self, width):
        self.x1 = 0
        self.x2 = width
        self.y = 400
        self.width = width

    def update(self, speed):
        self.x1 -= speed
        self.x2 -= speed

        if self.x1 <= -self.width:
            self.x1 = self.width

        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, screen):
        pygame.draw.rect(screen, (43, 9, 100), (self.x1, self.y, self.width, 10))
        pygame.draw.rect(screen, (43, 9, 100), (self.x2, self.y, self.width, 10))