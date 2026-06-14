import pygame
import random
import json
import os
from src.scenes.scene import Scene
from settings import FONT

class QuestionScene(Scene):
    def __init__(self, game, previous_scene, is_boss=False):
        super().__init__(game)
        self.previous_scene = previous_scene
        self.is_boss = is_boss 
        
        self.font_header = pygame.font.Font(FONT, 54)
        self.font_title = pygame.font.Font(FONT, 48)

        self.font_size = 36
        self.font_text = pygame.font.Font(FONT, self.font_size)
        
        reduced_time = int((self.previous_scene.speed - 6) * 15)
        base_time = 900 if self.is_boss else 600
        self.time_limit = max(120, base_time - reduced_time) 
        self.timer = self.time_limit
        
        self.state = "WAITING" 
        self.feedback_timer = 60 
        self.selected_key = None 
        self.option_keys = [pygame.K_1, pygame.K_2, pygame.K_3]
        
        self.key_map = {
            "1": pygame.K_1,
            "2": pygame.K_2,
            "3": pygame.K_3
        }
        
        self.questions = self.load_questions()
        self.current_q = random.choice(self.questions)

        self.question_lines = []
        self.wrapped_options = []
        self.optimize_font_size()

    def optimize_font_size(self):
        max_height = 320
        max_width = 640

        while self.font_size > 16:
            q_lines = self.wrap_text(self.current_q["q"], self.font_text, max_width)
            total_lines = len(q_lines)

            temp_wrapped_options = []
            for opt in self.current_q["options"]:
                o_lines = self.wrap_text(opt, self.font_text, max_width)
                temp_wrapped_options.append(o_lines)
                total_lines += len(o_lines)

            question_opts_space = 30
            space_between_opts = 15
            needed_height = (total_lines * self.font_text.get_height()) + question_opts_space + (len(self.current_q["options"]) - 1) * space_between_opts

            if needed_height <= max_height:
                self.question_lines = q_lines
                self.wrapped_options = temp_wrapped_options
                break
            else:
                self.font_size -= 2
                self.font_text = pygame.font.Font(FONT, self.font_size)

        else:
            self.question_lines = self.wrap_text(self.current_q["q"], self.font_text, max_width)
            self.wrapped_options = [self.wrap_text(opt, self.font_text, max_width) for opt in self.current_q["options"]]

    def load_questions(self):
        questions_path = "assets/perguntas_boss.json" if self.is_boss else "assets/perguntas.json"
        
        fallback_questions = [
            {
                "q": "Erro ao carregar JSON. A resposta é A?",
                "options": ["1) Sim", "2) Não", "3) Talvez"],
                "answer": pygame.K_1
            }
        ]

        if os.path.exists(questions_path):
            try:
                with open(questions_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    for q in data:
                        number = q.get("answer", "1").lower()
                        q["answer"] = self.key_map.get(number, pygame.K_1)

                    return data
            except json.JSONDecodeError:
                print(f"Aviso: O arquivo {questions_path} está com a formatação inválida.")
                return fallback_questions
        else:
            print(f"Aviso: Arquivo {questions_path} não encontrado.")
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
                self.previous_scene.apply_penalty()
                return
                
        elif self.state == "ANSWERED":
            self.feedback_timer -= 1
            if self.feedback_timer <= 0:
                if self.selected_key == self.current_q["answer"]:
                    self.previous_scene.apply_reward()
                    self.game.change_scene(self.previous_scene)
                else:
                    self.previous_scene.apply_penalty()

    def draw(self):
        self.previous_scene.draw()
        
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(220)
        if self.is_boss:
            overlay.fill((30, 10, 10))
        else:
            overlay.fill((20, 22, 30))
        self.game.screen.blit(overlay, (0, 0))

        if self.is_boss:
            bg_color = (40, 15, 20)
            border_color = (255, 85, 85)
            header_text = "! DESAFIO DO CHEFÃO !"
            header_color = (255, 85, 85)
        else:
            bg_color = (40, 42, 54)
            border_color = (139, 233, 253)
            header_text = "PERGUNTA"
            header_color = (80, 250, 123)

        card_rect = pygame.Rect(50, 60, 700, 480)
        pygame.draw.rect(self.game.screen, bg_color, card_rect, border_radius=15)
        pygame.draw.rect(self.game.screen, border_color, card_rect, width=3, border_radius=15)

        header_rend = self.font_header.render(header_text, True, header_color)
        header_pos = header_rend.get_rect(center=(400, 100))
        self.game.screen.blit(header_rend, header_pos)

        remaining_seconds = max(0, self.timer / 60)
        time_color = (255, 85, 85) if remaining_seconds <= 2.0 else (248, 248, 242)
        
        if self.state == "WAITING":
            time_text = self.font_title.render(f"TEMPO: {remaining_seconds:.1f}s", True, time_color)
            self.game.screen.blit(time_text, time_text.get_rect(center=(400, 150)))

        y_offset = 180 
        for line in self.question_lines:
            q_text = self.font_text.render(line, True, (241, 250, 140))
            self.game.screen.blit(q_text, (80, y_offset))
            y_offset += self.font_text.get_height() + 5 
            
        y_offset += 25

        for i, option_lines in enumerate(self.wrapped_options):
            current_option_key = self.option_keys[i]
            color = (248, 248, 242)
            
            if self.state == "ANSWERED":
                if current_option_key == self.current_q["answer"]:
                    color = (80, 250, 123)
                elif current_option_key == self.selected_key:
                    color = (255, 85, 85)
                else:
                    color = (98, 114, 164)

            for line in option_lines:
                opt_text = self.font_text.render(line, True, color)
                self.game.screen.blit(opt_text, (80, y_offset))
                y_offset += self.font_text.get_height() + 2

            y_offset += 15
