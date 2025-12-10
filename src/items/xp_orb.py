import pygame
from settings import *
from src.utils.helpers import AssetManager

class ExperienceGem(pygame.sprite.Sprite):
    def __init__(self, pos, xp_value, groups, player):
        super().__init__(groups)
        self.assets = AssetManager()
        self.player = player
        
        if xp_value < 10: color = 'xp_small'
        elif xp_value < 50: color = 'xp_medium'
        else: color = 'xp_large'
            
        self.image = self.assets.get_surface('xp_gem', (15, 15), color, 'circle')
        self.rect = self.image.get_rect(center=pos)
        
        # --- CORREÇÃO DO CRASH ---
        self.hitbox = self.rect.copy()
        
        self.xp_value = xp_value
        self.target = None
        self.speed = 0
        self.acceleration = 15

    def update(self, dt):
        if self.target:
            self.move_towards_target(dt)
        else:
            distance = pygame.math.Vector2(self.rect.center).distance_to(self.player.rect.center)
            if distance < self.player.magnet_radius:
                self.target = self.player

    def move_towards_target(self, dt):
        target_vec = pygame.math.Vector2(self.target.rect.center)
        my_vec = pygame.math.Vector2(self.rect.center)
        
        diff = target_vec - my_vec
        distance = diff.magnitude()
        
        if distance < 1:
            self.target.get_xp(self.xp_value)
            self.kill()
            return

        direction = diff.normalize()
        self.speed += self.acceleration
        
        movement_step = self.speed * dt * 60
        
        if movement_step >= distance:
            self.target.get_xp(self.xp_value)
            self.kill()
        else:
            new_pos = my_vec + direction * movement_step
            self.rect.center = (round(new_pos.x), round(new_pos.y))
            # Atualiza hitbox junto
            self.hitbox.center = self.rect.center