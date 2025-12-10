import pygame
import random
import math # Adicionado o import de math
from settings import *
from src.utils.helpers import AssetManager

class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, type_key, groups):
        super().__init__(groups)
        self.assets = AssetManager()
        self.type = type_key # 'heart', 'chest'
        
        # Configuração Visual
        if self.type == 'heart':
            # Usa 'pickup_heart' que é vermelho no settings
            self.image = self.assets.get_surface('pickup_heart', (16, 16), 'pickup_heart', 'circle')
            self.value = 30 
        elif self.type == 'chest':
            # CORREÇÃO AQUI: Mudado de 'gold' para 'pickup_chest'
            self.image = self.assets.get_surface('chest', (32, 32), 'pickup_chest', 'rect')
            self.value = 1 
            
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy()
        
        # Animação de flutuar (Bobbing)
        self.y_start = pos[1]
        self.bob_speed = 0.005
        self.bob_amount = 5
        self.spawn_time = pygame.time.get_ticks()

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        offset = math.sin(current_time * self.bob_speed) * self.bob_amount
        self.rect.centery = self.y_start + offset
        self.hitbox.center = self.rect.center