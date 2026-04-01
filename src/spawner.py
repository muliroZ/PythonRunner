import pygame
import random
from src.obstacle import Obstacle

class Spawner:
    def __init__(self, group):
        self.group = group
        self.timer = 0

    def update(self):
        self.timer += 1

        if self.timer > random.randint(60, 120):
            obstacle = Obstacle(800)
            self.group.add(obstacle)
            self.timer = 0