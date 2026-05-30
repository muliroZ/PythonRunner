import pygame
import random
import math
from src.scenes.scene import Scene
from src.scenes.game_over import GameOverScene
from src.scenes.question_scene import QuestionScene
from src.snake import Snake
from src.ground import Ground
from src.spawner import Spawner
from src.background import Background
from src.particles import Particle

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        pygame.mixer.music.play(-1)

        self.snake = Snake()
        self.snake_group = pygame.sprite.GroupSingle(self.snake)

        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.spawner = Spawner(self.obstacles, self.powerups)

        self.has_shield = False
        self.multiplier = 1
        self.multiplier_timer = 0

        self.ground = Ground(800)
        self.background = Background(800, 400)

        self.score = 0
        self.speed = 6
        self.font = pygame.font.Font(None, 36)

        self.last_question_score = 0

        self.particles: list[Particle] = []

        self.is_dead = False
        self.shake_timer = 0
        self.shake_intensity = 15

    def destroy_obstacles(self):
        for obstacle in self.obstacles:
            num_particles = random.randint(20, 35)
            explosion_color = (255, random.randint(100, 200), 0)

            for _ in range(num_particles):
                p = Particle(obstacle.rect.centerx, obstacle.rect.centery, explosion_color)
                self.particles.append(p)

        self.obstacles.empty()

    def apply_reward(self):
        self.score += 300
        self.destroy_obstacles()

        if "reward" in getattr(self.game, "sfx", {}):
            self.game.sfx["reward"].play()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.snake.jump()
                    if "jump" in self.game.sfx:
                        self.game.sfx["jump"].play()

    def update(self):
        if self.is_dead:
            self.shake_timer -= 1
            if self.shake_timer <= 0:
                pygame.mixer.music.stop()
                self.game.change_scene(GameOverScene(self.game, self.score))
            return
        
        if self.multiplier_timer > 0:
            self.multiplier_timer -= 1
            if self.multiplier_timer <= 0:
                self.multiplier = 1

        self.score += 1 * self.multiplier
        self.speed = 6 + (self.score // 200)

        if self.score > 0 and self.score % 1000 == 0 and self.score != self.last_question_score:
            self.last_question_score = self.score

            self.game.change_scene(QuestionScene(self.game, self))
            return

        self.snake_group.update()
        self.obstacles.update(self.speed)
        self.powerups.update(self.speed)
        self.spawner.update(self.speed)
        self.ground.update(self.speed)
        self.background.update(self.speed)

        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0:
                self.particles.remove(p)

        hit_powerups = pygame.sprite.spritecollide(self.snake, self.powerups, True)
        for hit in hit_powerups:
            if hit.type == "shield":
                self.has_shield = True
            elif hit.type == "multiplier":
                self.multiplier = 2
                self.multiplier_timer = 420

            if "reward" in getattr(self.game, "sfx", {}):
                self.game.sfx["reward"].play()

        hit_obstacles = pygame.sprite.spritecollide(self.snake, self.obstacles, False)
        if hit_obstacles:
            if self.has_shield:
                self.has_shield = False
                for obs in hit_obstacles:
                    for _ in range(15):
                        self.particles.append(Particle(obs.rect.centerx, obs.rect.centery, (139, 233, 253)))
                    self.destroy_obstacles()

                if "explosion" in getattr(self.game, "sfx", {}):
                    self.game.sfx["explosion"].play()
            
            else:
                self.is_dead = True
                self.shake_timer = 15
                if "hit" in getattr(self.game, "sfx", {}):
                    self.game.sfx["hit"].play()

    def draw(self):
        render_surface = pygame.Surface((800, 600))
        
        self.background.draw(render_surface)
        self.ground.draw(render_surface)

        self.powerups.draw(render_surface)

        if self.has_shield:
            pygame.draw.circle(render_surface, (139, 233, 253), self.snake.rect.center, 25, 4)

        self.snake_group.draw(render_surface)
        self.obstacles.draw(render_surface)
        
        for p in self.particles:
            p.draw(render_surface)
        
        if self.multiplier > 1:
            score_color = (255, int(math.sin(self.score * 0.1) * 127 + 128), 0)
        elif self.score < 1000:
            score_color = (248, 248, 242) # Branco / Off-white
        elif self.score < 1500:
            score_color = (80, 250, 123)  # Verde
        elif self.score < 2000:
            score_color = (139, 233, 253) # Ciano
        elif self.score < 2500:
            score_color = (255, 121, 198) # Rosa
        elif self.score < 3000:
            score_color = (189, 147, 249) # Roxo  
        else:
            r = int(math.sin(self.score * 0.1) * 127 + 128)
            g = int(math.sin(self.score * 0.1 + 2) * 127 + 128)
            b = int(math.sin(self.score * 0.1 + 4) * 127 + 128)
            score_color = (r, g, b)

        float_y = 10 + math.sin(self.score + 0.05) * 2

        score_text_str = f"Pontuação: {self.score}"
        if self.multiplier > 1:
            score_text_str += f" (x{self.multiplier})"

        score_shadow = self.font.render(score_text_str, True, (40, 42, 54))
        render_surface.blit(score_shadow, (12, float_y + 2))

        score_text_ui = self.font.render(score_text_str, True, score_color)
        render_surface.blit(score_text_ui, (10, float_y))

        offset_x = 0
        offset_y = 0
        
        if self.shake_timer > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(render_surface, (offset_x, offset_y))
