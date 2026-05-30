import pygame
import os
import json
from src.scenes.menu import MenuScene
from settings import WIDTH, HEIGHT, FPS, TITLE

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.high_score = self.load_high_score()
        self.state = "PLAYING"

        self.sfx = {}
        self.load_sfx()

        self.current_scene = MenuScene(self)

    def load_sfx(self):
        try:
            self.sfx['jump'] = pygame.mixer.Sound("assets/sounds/jump.wav")
            self.sfx['jump'].set_volume(0.3)

            self.sfx['hit'] = pygame.mixer.Sound("assets/sounds/hit.wav")
            self.sfx['reward'] = pygame.mixer.Sound("assets/sounds/reward.wav")
            self.sfx['explosion'] = pygame.mixer.Sound("assets/sounds/explosion.wav")

            pygame.mixer.music.load("assets/sounds/background_music.mp3")
            pygame.mixer.music.set_volume(0.5)

        except FileNotFoundError:
            print("Aviso: Ficheiros de áudio não encontrados na pasta assets/sounds/.")

    def load_high_score(self):
        if os.path.exists("score.json"):
            try:
                with open("score.json") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
            except json.JSONDecodeError:
                return 0
        return 0
    
    def save_high_score(self):
        with open("score.json", "w") as f:
            json.dump({"high_score": self.high_score}, f)

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
