import pygame
import math
from src.scenes.scene import Scene
from src.scenes.game_scene import GameScene
from src.background import Background

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        
        self.music = pygame.mixer.Sound("assets/sounds/menumusic.mp3")
        self.music.play(-1)

        self.font_title = pygame.font.Font(None, 80)
        self.font_start = pygame.font.Font(None, 48)

        self.background = Background(800, 400)
        self.timer = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.music.stop()
                    self.game.change_scene(GameScene(self.game))

    def update(self):
        self.background.update(1.5)
        self.timer += 1

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.background.draw(self.game.screen)
        
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(150)
        overlay.fill((40, 42, 54))
        self.game.screen.blit(overlay, (0, 0))

        title_text = "PYTHON RUNNER"
        title_shadow = self.font_title.render(title_text, True, (0, 0, 0))
        title = self.font_title.render(title_text, True, (80, 250, 123))
        
        self.game.screen.blit(title_shadow, (155, 155))
        self.game.screen.blit(title, (150, 150))

        alpha = abs(math.sin(self.timer * 0.05)) * 255
        start = self.font_start.render("Pressione ESPAÇO para Iniciar", True, (248, 248, 242))
        start.set_alpha(int(alpha))
        
        start_rect = start.get_rect(center=(400, 400))
        self.game.screen.blit(start, start_rect)