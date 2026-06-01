import pygame

class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except FileNotFoundError:
            self.sheet = None

    def get_image(self, frame_x, frame_y, width, height, scale = 1):
        image = pygame.Surface((width, height), pygame.SRCALPHA)

        if self.sheet:
            rect_cut = (frame_x * width, frame_y * height, width, height)
            image.blit(self.sheet, (0, 0), rect_cut)
        else:
            image.fill((255, 0, 255))

        if scale != 1:
            image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

        return image