import pygame
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, enemy_list):
        super().__init__(groups)
        self.image = pygame.image.load('assets/projectile.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center=pos)
        
        self.speed = 10
        self.damage = 10
        self.enemy_list = enemy_list
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 3000 # O tiro some depois de 3 seg se não acertar nada
        
        # Lógica simples de mirar no inimigo mais próximo
        self.direction = pygame.math.Vector2(1, 0) # Padrão pra direita
        self.target_closest_enemy(pos)

    def target_closest_enemy(self, player_pos):
        closest_dist = 5000
        closest_enemy = None
        
        # Procura quem tá mais perto
        for enemy in self.enemy_list:
            enemy_vec = pygame.math.Vector2(enemy.rect.center)
            player_vec = pygame.math.Vector2(player_pos)
            dist = (player_vec - enemy_vec).magnitude()
            
            if dist < closest_dist:
                closest_dist = dist
                closest_enemy = enemy
        
        if closest_enemy:
            enemy_vec = pygame.math.Vector2(closest_enemy.rect.center)
            my_pos = pygame.math.Vector2(player_pos)
            self.direction = (enemy_vec - my_pos).normalize()

    def update(self):
        self.rect.center += self.direction * self.speed
        
        # Remove se passar do tempo
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()