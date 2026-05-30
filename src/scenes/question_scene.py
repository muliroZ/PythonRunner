import pygame
import random
import os
import json
from src.scenes.scene import Scene
from src.scenes.game_over import GameOverScene

class QuestionScene(Scene):
    def __init__(self, game, previous_scene):
        super().__init__(game)
        self.previous_scene = previous_scene
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 36)
        
        reduced_time = int((previous_scene.speed - 6) * 15)
        self.time_limit = max(90, 900 - reduced_time)
        self.timer = self.time_limit
        
        self.state = "WAITING"
        self.feedback_timer = 60
        self.selected_key = None
        self.option_keys = [pygame.K_a, pygame.K_b, pygame.K_c]
        
        self.key_map = {
            'a': pygame.K_a,
            'b': pygame.K_b,
            'c': pygame.K_c
        }

        self.questions = self.load_questions()
        self.current_q = random.choice(self.questions)

    def load_questions(self):
        questions_path = "assets/perguntas.json"

        fallback_questions = [
            {
                "q": "Erro ao carregar JSON. A resposta é A?",
                "options": ["A) Sim", "B) Não", "C) Talvez"],
                "answer": pygame.K_a
            }
        ]

        if os.path.exists(questions_path):
            try:
                with open(questions_path, encoding="utf-8") as f:
                    data = json.load(f)

                    for q in data:
                        letter = q.get("answer", "a").lower()
                        q["answer"] = self.key_map.get(letter, pygame.K_a)

                return data
            except json.JSONDecodeError:
                print("Aviso: O arquivo perguntas.json está com a formatação inválida.")
                return fallback_questions

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]

        lines.append(' '.join(current_line))
        return lines

    def handle_events(self, events):
        if self.state == "WAITING":
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key in self.option_keys:
                        self.selected_key = event.key
                        self.state = "ANSWERED"

    def update(self):
        if self.state == "WAITING":
            self.timer -= 1
            if self.timer <= 0:
                self.game.change_scene(GameOverScene(self.game, self.previous_scene.score))
                
        elif self.state == "ANSWERED":
            self.feedback_timer -= 1
            if self.feedback_timer <= 0:
                if self.selected_key == self.current_q["answer"]:
                    self.previous_scene.apply_reward()
                    self.game.change_scene(self.previous_scene)
                else:
                    if "explosion" in getattr(self.game, "sfx", {}):
                        self.game.sfx["explosion"].play()

                    pygame.mixer.music.stop()

                    self.game.change_scene(GameOverScene(self.game, self.previous_scene.score))

    def draw(self):
        self.previous_scene.draw()
        
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))
        self.game.screen.blit(overlay, (0, 0))

        seconds_left = max(0, self.timer // 60)
        time_color = (255, 0, 0) if seconds_left <= 3 else (255, 255, 255)
        
        if self.state == "WAITING":
            time_text = self.font_title.render(f"TEMPO: {seconds_left}s", True, time_color)
            self.game.screen.blit(time_text, (330, 50))

        question_lines = self.wrap_text(self.current_q["q"], self.font_text, 700)

        y_offset = 150 
        for line in question_lines:
            q_text = self.font_text.render(line, True, (255, 255, 0))
            self.game.screen.blit(q_text, (50, y_offset))
            y_offset += self.font_text.get_height() + 5 
            
        y_offset += 40 

        for i, option in enumerate(self.current_q["options"]):
            current_option_key = self.option_keys[i]
            color = (200, 200, 200) 
            
            if self.state == "ANSWERED":
                if current_option_key == self.current_q["answer"]:
                    color = (0, 255, 0) 
                elif current_option_key == self.selected_key:
                    color = (255, 0, 0)
                else:
                    color = (100, 100, 100)

            opt_text = self.font_text.render(option, True, color)
            self.game.screen.blit(opt_text, (80, y_offset))
            y_offset += 50
