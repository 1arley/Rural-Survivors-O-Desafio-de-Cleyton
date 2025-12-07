import pygame
from .entity import Entity
from settings import *
from src.utils.helpers import AssetManager

class Player(Entity):
    def __init__(self, pos, groups, obstacles_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.assets = AssetManager()
        
        # --- CORREÇÃO VISUAL ---
        # Removemos target_size=(64,64) para não deformar.
        # O AssetManager agora vai detectar que a imagem é grande e ajustar a escala sozinha.
        self.image = self.assets.get_surface(
            key='player', 
            color_key='player_calouro'
        )
        
        self.rect = self.image.get_rect(topleft=pos)
        
        # Hitbox nos pés
        self.set_hitbox()
        
        # Stats
        self.stats = {'hp': 100, 'speed': 200, 'attack': 10}
        self.health = self.stats['hp']
        self.xp = 0
        self.level = 1
        self.next_level_xp = 10
        self.credits = 0 
        
        # Armas e Inventário
        self.weapons = [] 
        self.passives = []
        
        # Mecânicas
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.create_attack = create_attack 
        self.magnet_radius = 150 
        self.passives = []

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] or keys[pygame.K_UP]: self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: self.direction.y = 1
        else: self.direction.y = 0

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.direction.x = 1
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]: self.direction.x = -1
        else: self.direction.x = 0

    def get_xp(self, amount):
        self.xp += amount
        if self.xp >= self.next_level_xp:
            self.level_up()

    def level_up(self):
        self.xp -= self.next_level_xp
        self.level += 1
        self.next_level_xp = int(self.next_level_xp * 1.2)

    def update(self, dt):
        self.input()
        self.move(self.stats['speed'] * dt)
        
        if self.health < self.stats['hp']:
            self.health += 0.5 * dt