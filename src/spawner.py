import pygame
import random
from src.obstacle import Obstacle

class Spawner:
    def __init__(self, group):
        self.group = group
        self.timer = 0
        self.next_spawn = self.get_next_spawn(6)
        self.last_spawn_type = None

    def get_next_spawn(self, speed):
        base = random.randint(60, 120)
        return max(30, base - int(speed * 5))
    
    def get_obstacle_type(self, speed):
        if speed < 8:
            return random.choice(["small", "small", "tall", "flying"])
        else:
            return random.choice(["small", "tall", "tall", "flying", "flying"])
    
    def spawn_obstacle(self, speed):
        obstacle_type = self.get_obstacle_type(speed)

        if obstacle_type == self.last_spawn_type:
            obstacle_type = self.get_obstacle_type(speed)

        obstacle = Obstacle(800, obstacle_type)
        self.group.add(obstacle)

        self.last_spawn_type = obstacle_type

    def update(self, speed):
        self.timer += 1

        if self.timer >= self.next_spawn:
            self.spawn_obstacle(speed)

            self.timer = 0
            self.next_spawn = self.get_next_spawn(speed)
