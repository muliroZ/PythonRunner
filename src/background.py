import pygame
import random

class Layer:
    def __init__(self, image_path, width, height, y, speed):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.x1 = 0
        self.x2 = width
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def update(self, base_speed):
        move_speed = base_speed * self.speed

        self.x1 -= move_speed
        self.x2 -= move_speed

        if self.x1 <= -self.width:
            self.x1 = self.width

        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x1, self.y))
        screen.blit(self.image, (self.x2, self.y))


class WindParticle:
    def __init__(self, width):
        self.screen_width = width
        self.x = random.randint(0, width)
        # Distribui o vento entre as montanhas e o chão
        self.y = random.randint(250, 390) 
        self.length = random.randint(30, 100)
        # Move-se mais rápido que as camadas do fundo (efeito parallax acentuado)
        self.speed_multiplier = random.uniform(1.5, 2.5) 
        self.thickness = random.randint(1, 2)
        # Cor cinza-azulado para simular rajadas de vento
        self.color = (130, 140, 160)

    def update(self, base_speed):
        self.x -= base_speed * self.speed_multiplier
        
        # Reposiciona na direita com novas propriedades quando sai da tela
        if self.x + self.length < 0:
            self.x = self.screen_width + random.randint(10, 50)
            self.y = random.randint(200, 300)
            self.length = random.randint(30, 100)
            self.speed_multiplier = random.uniform(1.5, 2.5)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.length, self.thickness))


class Background:
    def __init__(self, width, height):
        self.width = width
        self.layers = [
            Layer("assets/version_c/layers/sky.png", width, height, 0, 0.05),
            Layer("assets/version_c/layers/clouds.png", width, height, 0, 0.1),
            Layer("assets/version_c/layers/far-mountains.png", width, height, 0, 0.2),
            Layer("assets/version_c/layers/canyon.png", width, height, 0, 0.3),
            Layer("assets/version_c/layers/front.png", width, height, 0, 0.5),
        ]

        self.particles = [WindParticle(width)]

    def update(self, speed):
        # Atualiza as camadas normais
        for layer in self.layers:
            layer.update(speed)
        
        target_particles = 1 + int((speed*0.7 - 6) * 4)
        
        # Adiciona novas partículas progressivamente
        while len(self.particles) < target_particles and speed:
            new_particle = WindParticle(self.width)
            # Força elas a nascerem fora da tela na direita, para não piscarem no meio do jogo
            new_particle.x = self.width + random.randint(0, 150) 
            self.particles.append(new_particle)

        for particle in self.particles:
            particle.update(speed)

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)
        
        for particle in self.particles:
            particle.draw(screen)