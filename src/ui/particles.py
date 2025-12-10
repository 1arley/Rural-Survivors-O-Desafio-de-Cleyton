import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color, groups):
        super().__init__(groups)
        self.pos = list(pos)
        
        # Física aleatória
        self.velocity = [random.uniform(-3, 3), random.uniform(-3, 3)]
        self.timer = random.randint(20, 40) # Tempo de vida
        
        # Tamanho inicial
        self.size = random.randint(4, 8)
        self.color = color
        
        # Cria a superfície
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        # Movimento
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        self.rect.center = self.pos
        
        # Reduz tamanho (efeito de desaparecer)
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
        else:
            # Reduz o sprite visualmente
            current_size = max(0, self.size * (self.timer / 40))
            self.image = pygame.transform.scale(self.image, (int(current_size), int(current_size)))