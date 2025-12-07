import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        
        # Variáveis base
        # self.image e self.rect serão definidos nas classes filhas

    def set_hitbox(self):
        """
        Define uma hitbox baseada nos pés da entidade.
        """
        if hasattr(self, 'rect'):
            # Ajuste aqui se achar a colisão muito gorda ou muito magra
            # 0.6 = 60% da largura da imagem
            width = self.rect.width * 0.6   
            # 0.3 = 30% da altura (apenas os pés)
            height = self.rect.height * 0.3 
            
            self.hitbox = pygame.Rect(0, 0, width, height)
            self.hitbox.midbottom = self.rect.midbottom
            # Sobe 1 pixel
            self.hitbox.y -= 1

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        # 1. Move a HITBOX (física)
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        
        # 2. Sincroniza a IMAGEM (visual)
        self.rect.midbottom = self.hitbox.midbottom

    def collision(self, direction):
        pass