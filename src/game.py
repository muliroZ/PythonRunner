import pygame
from src.snake import Snake
from src.ground import Ground
from src.spawner import Spawner
from src.background import Background
from settings import WIDTH, HEIGHT, FPS, TITLE

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.background = Background(800, 400)

        self.score = 0
        self.high_score = 0

        self.speed = 6

        self.font = pygame.font.Font(None, 36)

        self.snake = Snake()
        self.snake_group = pygame.sprite.GroupSingle(self.snake)

        self.obstacles = pygame.sprite.Group()
        self.spawner = Spawner(self.obstacles)

        self.ground = Ground(WIDTH)

        self.state = "PLAYING"

    def run(self):
        while self.state == "PLAYING" or self.state == "GAME_OVER":
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = "QUIT"

            if event.type == pygame.KEYDOWN:
                if self.state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        self.snake.jump()

                elif self.state == "GAME_OVER":
                    if event.key == pygame.K_SPACE:
                        self.restart()

    def restart(self):
        self.state = "PLAYING"
        self.score = 0
        self.speed = 6

        self.obstacles.empty()
        self.snake.rect.midbottom = (100, 300)
        self.snake.velocity_y = 0

    def update(self):
        if self.state == "PLAYING":
            self.score += 1
            self.speed = 6 + (self.score // 200)

            self.snake_group.update()
            self.obstacles.update(self.speed)
            self.spawner.update(self.speed)
            self.ground.update(self.speed)
            self.background.update(self.speed)

            if pygame.sprite.spritecollide(self.snake, self.obstacles, False):
                if self.score > self.high_score:
                    self.high_score = self.score

                self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill((30, 30, 30))

        self.background.draw(self.screen)
        self.ground.draw(self.screen)
        self.snake_group.draw(self.screen)
        self.obstacles.draw(self.screen)

        self.draw_score()

        if self.state == "GAME_OVER":
            self.draw_game_over()

        pygame.display.flip()

    def draw_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        high_score_text = self.font.render(f"Recorde: {self.high_score}", True, (255, 255, 0))

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))

    def draw_game_over(self):
        text = self.font.render("GAME OVER", True, (255, 0, 0))
        restart = self.font.render("Pressione ESPAÇO para reiniciar", True, (255, 255, 255))

        self.screen.blit(text, (300, 150))
        self.screen.blit(restart, (180, 200))
