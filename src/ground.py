import pygame

class Ground:
    def __init__(self, width):
        self.x1 = 0
        self.x2 = width
        self.y = 300
        self.speed = 6
        self.width = width

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -self.width:
            self.x1 = self.width

        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (self.x1, self.y, self.width, 10))
        pygame.draw.rect(screen, (200, 200, 200), (self.x2, self.y, self.width, 10))