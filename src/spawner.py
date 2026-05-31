import random
from src.obstacle import Obstacle
from src.powerup import PowerUp

class Spawner:
    def __init__(self, obstacle_group, powerup_group):
        self.obstacle_group = obstacle_group
        self.powerup_group = powerup_group
        self.timer = 0
        self.last_spawn_type = None
        self.powerup_timer = 300
        self.last_spawn_was_cluster = False

        self.next_spawn = self.get_next_spawn(6)

    def get_next_spawn(self, speed):
        base = random.randint(60, 120)
        breath = 40 if self.last_spawn_was_cluster else 0

        return max(35, base - int(speed * 5)) + breath
    
    def get_obstacle_type(self, speed):
        if speed < 8:
            return random.choice(["small", "small", "tall", "flying"])
        elif speed < 12:
            return random.choice(["small", "tall", "tall", "flying", "flying"])
        else:
            return random.choice(["tall", "flying", "flying"])
    
    def spawn_obstacle(self, speed):
        obstacle_type = self.get_obstacle_type(speed)

        if obstacle_type == self.last_spawn_type:
            obstacle_type = self.get_obstacle_type(speed)

        is_cluster = speed >= 9 and random.random() < 0.3
        self.last_spawn_was_cluster = is_cluster

        obstacle = Obstacle(800, obstacle_type)
        self.obstacle_group.add(obstacle)

        if is_cluster:
            secondary_type = "small" if obstacle_type == "flying" else "flying"
            extra_distance = random.randint(250, 400)

            obstacle2 = Obstacle(800 + extra_distance, secondary_type)
            self.obstacle_group.add(obstacle2)

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
