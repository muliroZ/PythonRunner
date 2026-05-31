import pygame
from src.scenes.scene import Scene
from src.background import Background
from settings import FONT

class GameOverScene(Scene):
    def __init__(self, game, score):
        super().__init__(game)

        self.music = pygame.mixer.Sound("assets/sounds/gameover.mp3")
        self.music.play(-1)

        self.score = score
        self.font_title = pygame.font.Font(FONT, 80)
        self.font_text = pygame.font.Font(FONT, 48)
        self.font_small = pygame.font.Font(FONT, 36)

        self.background = Background(800, 400)

        self.new_record = False
        if score > self.game.high_score:
            self.game.high_score = score
            self.game.save_high_score()
            self.new_record = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.music.stop()
                    from src.scenes.game_scene import GameScene

                    self.game.change_scene(GameScene(self.game))

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.background.draw(self.game.screen)

        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(180)
        overlay.fill((60, 20, 20))
        self.game.screen.blit(overlay, (0, 0))

        title_shadow = self.font_title.render("GAME OVER", True, (0, 0, 0))
        title = self.font_title.render("GAME OVER", True, (255, 85, 85)) # Vermelho vibrante
        self.game.screen.blit(title_shadow, (235, 105))
        self.game.screen.blit(title, (230, 100))

        pygame.draw.rect(self.game.screen, (40, 42, 54), (250, 220, 300, 140), border_radius=15)
        pygame.draw.rect(self.game.screen, (98, 114, 164), (250, 220, 300, 140), width=3, border_radius=15)

        score_text = self.font_text.render(f"Pontuação: {self.score}", True, (248, 248, 242))
        score_rect = score_text.get_rect(center=(400, 260))
        self.game.screen.blit(score_text, score_rect)

        if self.new_record:
            high_text = self.font_small.render("NOVO RECORDE!", True, (241, 250, 140))
        else:
            high_text = self.font_small.render(f"Recorde: {self.game.high_score}", True, (189, 147, 249))
            
        high_rect = high_text.get_rect(center=(400, 320))
        self.game.screen.blit(high_text, high_rect)

        restart = self.font_small.render("Pressione ESPAÇO para tentar de novo", True, (200, 200, 200))
        restart_rect = restart.get_rect(center=(400, 450))
        self.game.screen.blit(restart, restart_rect)
