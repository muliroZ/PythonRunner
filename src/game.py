import pygame
from src.snake import Snake
from src.ground import Ground
from src.spawner import Spawner
from settings import WIDTH, HEIGHT, FPS, TITLE

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.snake = Snake()
        self.snake_group = pygame.sprite.GroupSingle(self.snake)

        self.obstacles = pygame.sprite.Group()
        self.spawner = Spawner(self.obstacles)

        self.ground = Ground(WIDTH)

        self.running = True

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.snake.jump()

    def update(self):
        self.snake_group.update()
        self.obstacles.update()
        self.spawner.update()
        self.ground.update()

        if pygame.sprite.spritecollide(self.snake, self.obstacles, False):
            print("Game Over")
            self.running = False

    def draw(self):
        self.screen.fill((30, 30, 30))

        self.ground.draw(self.screen)
        self.snake_group.draw(self.screen)
        self.obstacles.draw(self.screen)

        pygame.display.flip()
