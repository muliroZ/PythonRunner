import pygame

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.normal_image = pygame.Surface((30, 50))
        self.normal_image.fill((80, 250, 123))

        self.slide_image = pygame.Surface((50, 25))
        self.slide_image.fill((80, 250, 123))

        self.image = self.normal_image
        self.rect = self.image.get_rect(midbottom=(100, 400))

        self.gravity = 0
        self.is_sliding = False
        self.slide_timer = 0

    def jump(self):
        if self.rect.bottom >= 400 and not self.is_sliding:
            self.gravity -= 15
            return True
        return False

    def slide(self):
        if self.rect.bottom >= 400 and not self.is_sliding:
            self.is_sliding = True
            self.slide_timer = 30

            self.image = self.slide_image
            old_midbottom = self.rect.midbottom
            self.rect = self.image.get_rect(midbottom=old_midbottom)
            return True
        return False

    def update(self):
        self.gravity += 0.8
        self.rect.y += int(self.gravity)

        if self.rect.bottom >= 400:
            self.rect.bottom = 400
            self.gravity = 0

        if self.is_sliding:
            self.slide_timer -= 1
            if self.slide_timer <= 0:
                self.is_sliding = False
                self.image = self.normal_image

                old_midbottom = self.rect.midbottom
                self.rect = self.image.get_rect(midbottom=old_midbottom)
