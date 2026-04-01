import pygame
from src.scenes.menu import MenuScene
from settings import WIDTH, HEIGHT, FPS, TITLE

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.high_score = 0

        self.state = "PLAYING"

        self.current_scene = MenuScene(self)

    def change_scene(self, new_scene):
        self.current_scene = new_scene

    def run(self):
        while self.state == "PLAYING" or self.state == "GAME_OVER":
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.state = "CLOSED"
            
            self.current_scene.handle_events(events)
            self.current_scene.update()
            self.current_scene.draw()

            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
