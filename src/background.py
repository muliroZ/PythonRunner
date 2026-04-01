import pygame

class Layer:
    def __init__(self, width, height, y, speed, color):
        self.x1 = 0
        self.x2 = width
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color

    def update(self, base_speed):
        move_speed = base_speed * self.speed

        self.x1 -= move_speed
        self.x2 -= move_speed

        if self.x1 <= -self.width:
            self.x1 = self.width

        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x1, self.y, self.width, self.height))
        pygame.draw.rect(screen, self.color, (self.x2, self.y, self.width, self.height))


class Background:
    def __init__(self, width, height):
        self.layers = [
            Layer(width, height, 0, 0.2, (20, 20, 40)),   # céu
            Layer(width, 100, 200, 0.4, (50, 50, 80)),    # montanhas
        ]

    def update(self, speed):
        for layer in self.layers:
            layer.update(speed)

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)