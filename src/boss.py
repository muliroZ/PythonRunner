import pygame
import math
import random

class Laser(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        
        original_image = pygame.Surface((60, 20), pygame.SRCALPHA)
        pygame.draw.rect(original_image, (255, 85, 85), (0, 0, 60, 20), border_radius=10) 
        pygame.draw.rect(original_image, (255, 255, 255), (10, 5, 40, 10), border_radius=5) 
        
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.hypot(dx, dy)
        
        if distance != 0:
            self.dir_x = dx / distance
            self.dir_y = dy / distance
        else:
            self.dir_x = -1
            self.dir_y = 0

        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(original_image, angle)
        
        self.rect = self.image.get_rect(center=(start_x, start_y))
        
        self.pos_x = float(start_x)
        self.pos_y = float(start_y)
        
        self.speed = 15

    def update(self, speed):
        self.pos_x += self.dir_x * self.speed
        self.pos_y += self.dir_y * self.speed
        
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)

        if self.rect.right < 0 or self.rect.left > 800 or self.rect.top > 600 or self.rect.bottom < 0:
            self.kill()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 100), pygame.SRCALPHA)
        self.image.fill((189, 147, 249))
        self.rect = self.image.get_rect(center=(900, 200))

        self.target_x = 700
        self.base_y = 200
        self.timer = 0
        self.health = 3
        self.laser_timer = 60

    def update(self, laser_group, player_rect):
        if self.rect.centerx > self.target_x:
            self.rect.x -= 2
        
        self.timer += 0.05
        offset_y = math.sin(self.timer) * 80 + math.sin(self.timer * 0.5) * 40
        self.rect.y = self.base_y + int(offset_y)

        self.laser_timer -= 1
        if self.laser_timer <= 0:
            laser = Laser(self.rect.left, self.rect.centery, player_rect.centerx, player_rect.centery)
            laser_group.add(laser)
            
            self.laser_timer = random.randint(30, 90)
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)