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
from src.boss import Boss, Laser
from settings import FONT

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
        self.frames_survived = 0
        self.speed = 6
        self.font = pygame.font.Font(FONT, 36)

        self.last_question_score = 0

        self.particles: list[Particle] = []

        self.is_dead = False
        self.shake_timer = 0
        self.shake_intensity = 15

        self.lives = 3

        self.lasers = pygame.sprite.Group()
        self.boss = None
        self.boss_fight_active = False
        self.boss_defeated = False

        self.boss_warning_active = False
        self.boss_warning_timer = 0
        self.boss_defeated_message_active = False
        self.boss_defeated_timer = 0

        self.phase = 1

    def destroy_group(self, group):
        for member in group:
            num_particles = random.randint(20, 35)
            explosion_color = (255, random.randint(100, 200), 0)

            for _ in range(num_particles):
                p = Particle(member.rect.centerx, member.rect.centery, explosion_color)
                self.particles.append(p)

        group.empty()

    def apply_reward(self):
        if "reward" in getattr(self.game, "sfx", {}):
            self.game.sfx["reward"].play()

        if self.boss_fight_active and self.boss:
            self.boss.health -= 1
            self.destroy_group(self.lasers)
            
            match random.choice(["shield", "multiplier"]):
                case "shield":
                    self.has_shield = True
                case "multiplier":
                    self.multiplier = 2
                    self.multiplier_timer = 300

            if self.boss.health <= 0:
                self.boss_fight_active = False
                self.boss = None
                self.boss_defeated = True

                self.score += 2000
                self.boss_defeated_message_active = True
                self.boss_defeated_timer = 180

                for _ in range(50):
                    self.particles.append(Particle(700, 300, (189, 147, 249)))
                self.destroy_group(self.lasers)
                self.destroy_group(self.obstacles)
                return

        self.score += 300
        self.destroy_group(self.obstacles)

    def apply_penalty(self):
        self.lives -= 1
        self.score -= max(0, self.score - 750)

        if self.lives <= 0:
            if "explosion" in getattr(self.game, "sfx", {}):
                self.game.sfx["explosion"].play()
            pygame.mixer.music.stop()

            self.game.change_scene(GameOverScene(self.game, self.score))
        else:
            if "hit" in getattr(self.game, "sfx", {}):
                self.game.sfx["hit"].play()

            self.destroy_group(self.obstacles)
            self.destroy_group(self.lasers)
            self.game.change_scene(self)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:
                    if self.snake.jump():
                        if "jump" in self.game.sfx:
                            self.game.sfx["jump"].play()

                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    if self.snake.slide():
                        if "dash" in getattr(self.game, "sfx", {}):
                            self.game.sfx["dash"].play()

    def update(self):
        if self.is_dead:
            self.shake_timer -= 1
            if self.shake_timer <= 0:
                pygame.mixer.music.stop()
                self.game.change_scene(GameOverScene(self.game, self.score))
            return

        if self.frames_survived >= 2500 and not self.boss_fight_active and self.boss is None and not self.boss_defeated and not self.boss_warning_active:
            self.boss_warning_active = True
            self.boss_warning_timer = 180
            self.destroy_group(self.obstacles)
            self.destroy_group(self.powerups)
        
        if self.multiplier_timer > 0:
            self.multiplier_timer -= 1
            if self.multiplier_timer <= 0:
                self.multiplier = 1

        self.score += 1 * self.multiplier
        self.frames_survived += 1

        if self.phase == 1:
            new_speed = 6 + (self.frames_survived // 400)
            self.speed = min(new_speed, 16)
        else:
            new_speed = 9 + (self.frames_survived // 300)
            self.speed = min(new_speed, 20)

        self.snake_group.update()
        self.ground.update(self.speed)
        self.background.update(self.speed)

        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0:
                self.particles.remove(p)

        if self.boss_warning_active:
            self.boss_warning_timer -= 1
            if self.boss_warning_timer <= 0:
                self.boss_warning_active = False
                self.boss_fight_active = True
                self.boss = Boss()
        
        elif self.boss_fight_active:
            self.lasers.update(self.speed)
            has_shooted = self.boss.update(self.lasers, self.snake.hitbox)

            if has_shooted and "jump" in getattr(self.game, "sfx", {}):
                self.game.sfx["jump"].play()

            if self.frames_survived % 600 == 0 and self.score != self.last_question_score:
                self.last_question_score = self.score
                self.game.change_scene(QuestionScene(self.game, self, is_boss=True))
                return
            
            if pygame.sprite.spritecollide(self.snake, self.lasers, False, collided=lambda p, obj: p.hitbox.colliderect(obj.rect)):
                if self.has_shield:
                    self.has_shield = False
                    if "explosion" in getattr(self.game, "sfx", {}):
                        self.game.sfx["explosion"].play()
                    self.destroy_group(self.lasers)
                else:
                    self.apply_penalty()

        elif self.boss_defeated_message_active:
            self.boss_defeated_timer -= 1
            if self.boss_defeated_timer <= 0:
                self.boss_defeated_message_active = False
                
                self.phase = 2
                self.frames_survived = 0
        else:
            self.spawner.update(self.speed)
            self.obstacles.update(self.speed)
            self.powerups.update(self.speed)

            if self.frames_survived > 0 and self.frames_survived % 1000 == 0 and self.score != self.last_question_score:
                self.last_question_score = self.score

                self.game.change_scene(QuestionScene(self.game, self))
                return

            hit_powerups = pygame.sprite.spritecollide(self.snake, self.powerups, True, collided=lambda p, obj: p.hitbox.colliderect(obj.rect))
            for hit in hit_powerups:
                if hit.type == "shield":
                    self.has_shield = True
                elif hit.type == "multiplier":
                    self.multiplier = 2
                    self.multiplier_timer = 420

                if "reward" in getattr(self.game, "sfx", {}):
                    self.game.sfx["reward"].play()

            hit_obstacles = pygame.sprite.spritecollide(self.snake, self.obstacles, False, collided=lambda p, obj: p.hitbox.colliderect(obj.rect))
            if hit_obstacles:
                if self.has_shield:
                    self.has_shield = False
                    for obs in hit_obstacles:
                        for _ in range(15):
                            self.particles.append(Particle(obs.rect.centerx, obs.rect.centery, (139, 233, 253)))
                        self.destroy_group(self.obstacles)

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

        if self.phase == 2:
            night_filter = pygame.Surface((800, 600))
            night_filter.set_alpha(160)
            night_filter.fill((15, 15, 45))
            render_surface.blit(night_filter, (0, 0))

        self.powerups.draw(render_surface)

        if self.has_shield:
            pygame.draw.circle(render_surface, (139, 233, 253), self.snake.hitbox.center, 25, 4)

        self.snake_group.draw(render_surface)
        self.obstacles.draw(render_surface)

        if self.boss_fight_active and self.boss:
            self.boss.draw(render_surface)
            self.lasers.draw(render_surface)
        
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

        lives_text_str = f"Vidas: {self.lives}"
        lives_color = (255, 85, 85) if self.lives == 1 else (139, 233, 253)

        lives_shadow = self.font.render(lives_text_str, True, (40, 42, 54))
        render_surface.blit(lives_shadow, (12, float_y + 37))

        lives_text_ui = self.font.render(lives_text_str, True, lives_color)
        render_surface.blit(lives_text_ui, (10, float_y + 35))

        if self.boss_warning_active:
            alpha = int(abs(math.sin(self.boss_warning_timer * 0.1)) * 100)
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(alpha)
            overlay.fill((255, 0, 0))
            render_surface.blit(overlay, (0, 0))

            warning_text = self.font.render("! CHEFÃO CHEGANDO !", True, (255, 85, 85))
            text_rect = warning_text.get_rect(center=(400, 250))
            render_surface.blit(warning_text, text_rect)

        elif self.boss_defeated_message_active:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(150)
            overlay.fill((40, 42, 54))
            render_surface.blit(overlay, (0, 0))

            congrats_text = self.font.render("CHEFÃO DERROTADO, PARABÉNS !", True, (80, 250, 123))
            text_rect = congrats_text.get_rect(center=(400, 250))
            render_surface.blit(congrats_text, text_rect)

            sub_text = self.font.render("Iniciando Módulo de Alta Performance...", True, (248, 248, 242))
            sub_rect = sub_text.get_rect(center=(400, 300))
            render_surface.blit(sub_text, sub_rect)

        offset_x = 0
        offset_y = 0
        
        if self.shake_timer > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)

        self.game.screen.fill((0, 0, 0))
        self.game.screen.blit(render_surface, (offset_x, offset_y))
