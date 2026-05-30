import random
from src.obstacle import Obstacle
from src.powerup import PowerUp

class Spawner:
    def __init__(self, obstacle_group, powerup_group):
        self.obstacle_group = obstacle_group
        self.powerup_group = powerup_group
        self.timer = 0
        self.next_spawn = self.get_next_spawn(6)
        self.last_spawn_type = None
        self.powerup_timer = 300

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
        self.obstacle_group.add(obstacle)

        self.last_spawn_type = obstacle_type

    def spawn_powerup(self):
        p_type = random.choice(["shield", "multiplier"])
        
        p_up = PowerUp(900, p_type)
        self.powerup_group.add(p_up)

        self.powerup_timer = random.randint(600, 1200)

    def update(self, speed):
        self.timer += 1
        self.powerup_timer -= 1

        if self.timer >= self.next_spawn:
            self.spawn_obstacle(speed)

            self.timer = 0
            self.next_spawn = self.get_next_spawn(speed)

        if self.powerup_timer <= 0:
            self.spawn_powerup()
