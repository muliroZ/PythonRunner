import pygame
from src.spritesheet import SpriteSheet

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_sheet_walk = SpriteSheet("assets/sprites/PythonicaWalk.png")
        self.sprite_sheet_jump = SpriteSheet("assets/sprites/PythonicaJump.png")
        self.sprite_sheet_dash = SpriteSheet("assets/sprites/PythonicaSlide.png")
        
        self.run_frames = [self.sprite_sheet_walk.get_image(i, 0, 42, 42, scale=2) for i in range(10)]
        self.jump_frames = [self.sprite_sheet_jump.get_image(i, 0, 42, 42, scale=2) for i in range(11)]
        self.dash_frames = [self.sprite_sheet_dash.get_image(i, 0, 42, 42, scale=2) for i in range(11)]

        self.animation_index = 0
        self.current_state = "run"

        self.image = self.run_frames[self.animation_index]
        self.rect = self.image.get_rect()

        self.hitbox = pygame.Rect(0, 0, 30, 50)
        self.hitbox.midbottom = (100, 400)

        self.gravity = 0
        self.is_sliding = False
        self.slide_timer = 0

    def animate(self):
        new_state = "run"
        if self.is_sliding:
            new_state = "dash"
        elif self.hitbox.bottom < 400:
            new_state = "jump"
        
        if new_state != self.current_state:
            self.current_state = new_state
            self.animation_index = 0

        if self.current_state == "dash":
            frames = self.dash_frames
        elif self.current_state == "jump":
            frames = self.jump_frames
        else:
            frames = self.run_frames

        self.animation_index += 0.2

        if self.animation_index >= len(frames):
            if self.current_state == "run":
                self.animation_index = 0
            else:
                self.animation_index = len(frames) - 1

        self.image = frames[int(self.animation_index)]

    def jump(self):
        if self.hitbox.bottom >= 400 and not self.is_sliding:
            self.gravity = -15

            return True
        return False

    def slide(self):
        if self.hitbox.bottom >= 400 and not self.is_sliding:
            self.is_sliding = True
            self.slide_timer = 30
            
            old_midbottom = self.hitbox.midbottom
            self.image = self.dash_frames[0]
            self.hitbox = pygame.Rect(0, 0, 50, 25)
            self.hitbox.midbottom = old_midbottom

            return True
        return False

    def update(self):
        self.animate()

        self.gravity += 0.8
        self.hitbox.y += int(self.gravity)

        if self.hitbox.bottom >= 400:
            self.hitbox.bottom = 400
            self.gravity = 0

        if self.is_sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.is_sliding = False
                
                old_midbottom = self.rect.midbottom
                self.image = self.run_frames[0]
                self.hitbox = pygame.Rect(0, 0, 30, 50)
                self.hitbox.midbottom = old_midbottom
        
        self.rect.midbottom = self.hitbox.midbottom
