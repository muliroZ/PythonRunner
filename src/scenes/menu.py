import pygame
from src.scenes.scene import Scene
from src.scenes.game_scene import GameScene

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 48)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game.change_scene(GameScene(self.game))

    def draw(self):
        self.game.screen.fill((0, 0, 0))

        title = self.font.render("Snake Runner", True, (255, 255, 255))
        start = self.font.render("Pressione ESPAÇO", True, (200, 200, 200))

        self.game.screen.blit(title, (250, 150))
        self.game.screen.blit(start, (230, 220))