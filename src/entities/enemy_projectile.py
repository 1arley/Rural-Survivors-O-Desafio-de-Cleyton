import pygame
from settings import *
from src.utils.helpers import AssetManager

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, damage, groups):
        super().__init__(groups)
        self.assets = AssetManager()
        self.image = self.assets.get_surface('proj_enemy', (15, 15), 'proj_enemy', 'circle')
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy()
        
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.spawn_time = pygame.time.get_ticks()
        self.life = 3000 # 3 segundos de vida

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        self.hitbox.center = self.rect.center
        
        if pygame.time.get_ticks() - self.spawn_time > self.life:
            self.kill()