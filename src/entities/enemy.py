import pygame
from .entity import Entity
from settings import *
from src.utils.helpers import AssetManager

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, player, stats):
        super().__init__(groups)
        self.player = player
        self.assets = AssetManager()
        
        # Define cor baseada no tipo
        color_key = 'enemy_basic'
        if monster_name == 'trabalho_grupo': color_key = 'enemy_fast'
        elif monster_name == 'prova_final': color_key = 'enemy_tank'
        elif monster_name == 'tcc': color_key = 'enemy_boss'
            
        self.image = self.assets.get_surface(monster_name, (40, 40), color_key, 'rect')
        self.rect = self.image.get_rect(topleft=pos)
        self.set_hitbox()
        
        # Stats do JSON
        self.speed = stats['speed']
        self.health = stats['hp']
        self.damage = stats['damage']
        self.xp_value = stats['xp']
        
    def get_player_distance_direction(self):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(self.player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def update(self, dt):
        dist, dir = self.get_player_distance_direction()
        self.direction = dir
        self.move(self.speed * dt)