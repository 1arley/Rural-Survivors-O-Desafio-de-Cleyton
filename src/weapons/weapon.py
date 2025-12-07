import pygame
import math
from settings import *
from src.utils.helpers import AssetManager

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, damage, life, groups, color_key):
        super().__init__(groups)
        self.assets = AssetManager()
        self.image = self.assets.get_surface('proj', (15, 15), color_key, 'circle')
        self.rect = self.image.get_rect(center=pos)
        
        # --- CORREÇÃO DO CRASH ---
        # Todo sprite precisa ter hitbox se o debug da camera estiver ligado
        self.hitbox = self.rect.copy()
        
        self.direction = direction
        self.speed = speed
        self.damage = damage
        self.spawn_time = pygame.time.get_ticks()
        self.life = life

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        # Sincroniza a hitbox com o movimento
        self.hitbox.center = self.rect.center
        
        if pygame.time.get_ticks() - self.spawn_time > self.life:
            self.kill()

class WeaponController:
    def __init__(self, player, groups):
        self.player = player
        self.groups = groups
        self.weapons_data = {
            'caderno': {'lvl': 1, 'cooldown': 1000, 'last_shot': 0, 'damage': 10},
        }
        
    def add_weapon(self, name):
        if name not in self.weapons_data:
            self.weapons_data[name] = {'lvl': 1, 'cooldown': 1000, 'last_shot': 0, 'damage': 10}

    def update(self):
        current_time = pygame.time.get_ticks()
        for name, data in self.weapons_data.items():
            if current_time - data['last_shot'] >= data['cooldown']:
                self.fire(name, data)
                data['last_shot'] = current_time
    
    def fire(self, name, data):
        if not self.groups['enemy_sprites']:
            target_dir = pygame.math.Vector2(1, 0)
        else:
            closest = min([e for e in self.groups['enemy_sprites']], 
                          key=lambda e: pygame.math.Vector2(e.rect.center).distance_to(self.player.rect.center))
            
            p_pos = pygame.math.Vector2(self.player.rect.center)
            e_pos = pygame.math.Vector2(closest.rect.center)
            target_dir = (e_pos - p_pos).normalize()

        if name == 'caderno':
            Projectile(self.player.rect.center, target_dir, 400, data['damage'], 2000, 
                       [self.groups['all_sprites'], self.groups['attack_sprites']], 'proj_caderno')
            
        elif name == 'caneta':
            Projectile(self.player.rect.center, target_dir, 600, data['damage'], 3000,
                       [self.groups['all_sprites'], self.groups['attack_sprites']], 'proj_caneta')