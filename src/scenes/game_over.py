import pygame
from src.scenes.scene import Scene

class GameOverScene(Scene):
    def __init__(self, game, score):
        super().__init__(game)
        self.score = score
        self.font = pygame.font.Font(None, 48)

        if score > self.game.high_score:
            self.game.high_score = score

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    from src.scenes.game_scene import GameScene

                    self.game.change_scene(GameScene(self.game))

    def draw(self):
        self.game.screen.fill((0, 0, 0))

        text = self.font.render("GAME OVER", True, (255, 0, 0))
        score = self.font.render(f"Score: {self.score}", True, (255,255,255))
        high = self.font.render(f"Recorde: {self.game.high_score}", True, (255,255,0))
        restart = self.font.render("Pressione ESPAÇO", True, (200,200,200))

        self.game.screen.blit(text, (260, 120))
        self.game.screen.blit(score, (280, 180))
        self.game.screen.blit(high, (260, 230))
        self.game.screen.blit(restart, (220, 300))
