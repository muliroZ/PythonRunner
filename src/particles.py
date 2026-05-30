import pygame
import random

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        
        self.size = random.randint(3, 8)
        
        self.vel_x = random.uniform(-6, 6)
        self.vel_y = random.uniform(-12, -2)
        
        self.lifetime = random.randint(30, 60)
        self.gravity = 0.5

    def update(self):
        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y
        
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            rect = (int(self.x), int(self.y), self.size, self.size)
            pygame.draw.rect(screen, self.color, rect)