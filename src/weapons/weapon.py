import pygame
from settings import *

class AttackSprite(pygame.sprite.Sprite):
    def __init__(self, groups, damage, type_str):
        super().__init__(groups)
        self.damage = damage
        self.type = type_str 
        self.hit_list = []

class Weapon:
    def __init__(self, player, groups, data):
        self.player = player
        self.groups = groups
        self.data = data
        
        self.lvl = 1
        
        # Atributos Base (Lidos do JSON)
        self.base_damage = data['damage']
        self.base_cooldown = data['cooldown']
        # self.base_area não existe como atributo direto, é lido do data
        
        # Atributos Atuais (Que mudam com nível)
        self.damage = self.base_damage
        self.cooldown = self.base_cooldown
        
        self.last_shot = 0
        self.name = data['name']
        self.type = data.get('type', 'projectile')
        self.key = None 

    def upgrade(self):
        """Aplica os bônus definidos em 'per_level' no JSON."""
        self.lvl += 1
        
        per_level = self.data.get('per_level', {})
        
        # Aplica bônus aditivos
        self.damage += per_level.get('damage', 0)
        self.cooldown += per_level.get('cooldown', 0) # Geralmente negativo
        
        # Para atributos que ficam dentro de 'data' (como area, speed),
        # precisamos atualizar o dicionário self.data
        if 'speed' in per_level:
            self.data['speed'] += per_level['speed']
        if 'area' in per_level:
            self.data['area'] = self.data.get('area', 1.0) + per_level['area']
        if 'scale' in per_level:
            self.data['scale'] = self.data.get('scale', 1.0) + per_level['scale']
            
        print(f"{self.name} upou para Lv {self.lvl}! Dano: {self.damage}")

    def update(self):
        now = pygame.time.get_ticks()
        real_cooldown = self.cooldown * (1.0 + self.player.modifiers['cooldown']) 
        real_cooldown = max(100, real_cooldown) # Limite mínimo de 0.1s
        
        if now - self.last_shot >= real_cooldown:
            self.activate()
            self.last_shot = now
    
    def activate(self):
        raise NotImplementedError