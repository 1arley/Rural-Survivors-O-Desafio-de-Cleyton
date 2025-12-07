# entity.py
import pygame
from settings import *

class Character(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        # Atributos comuns a todos os seres
        self.direction = pygame.math.Vector2()
        self.speed = 0
        self.health = 10  # Valor padrão, pode ser sobrescrito pelos filhos
        
        # Placeholders para imagem e rect (serão definidos nos filhos)
        self.image = None 
        self.rect = None

    def move(self, speed):
        # Lógica de física compartilhada
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # Atualiza a posição
        self.rect.center += self.direction * speed

    def take_damage(self, amount):
        self.health -= amount
        
        # Feedback visual no console (útil para debug agora)
        print(f"{type(self).__name__} recebeu {amount} de dano. Vida: {self.health}")

        if self.health <= 0:
            self.die()

    def die(self):
        self.kill()