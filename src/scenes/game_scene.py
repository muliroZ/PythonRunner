import pygame
from src.scenes.scene import Scene
from src.snake import Snake
from src.ground import Ground
from src.spawner import Spawner
from src.background import Background

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.snake = Snake()
        self.snake_group = pygame.sprite.GroupSingle(self.snake)

        self.obstacles = pygame.sprite.Group()
        self.spawner = Spawner(self.obstacles)

        self.ground = Ground(800)
        self.background = Background(800, 400)

        self.score = 0
        self.speed = 6
        self.font = pygame.font.Font(None, 36)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.snake.jump()

    def update(self):
        self.score += 1
        self.speed = 6 + (self.score // 200)

        self.snake_group.update()
        self.obstacles.update(self.speed)
        self.spawner.update(self.speed)
        self.ground.update(self.speed)
        self.background.update(self.speed)

        if pygame.sprite.spritecollide(self.snake, self.obstacles, False):
            from src.scenes.game_over import GameOverScene
            
            self.game.change_scene(
                GameOverScene(self.game, self.score)
            )

    def draw(self):
        self.background.draw(self.game.screen)
        self.ground.draw(self.game.screen)

        self.snake_group.draw(self.game.screen)
        self.obstacles.draw(self.game.screen)

        score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        self.game.screen.blit(score_text, (10, 10))