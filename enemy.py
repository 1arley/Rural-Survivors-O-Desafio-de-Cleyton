import pygame
from settings import *
from entity import Character
from item import ExperienceOrb

class Enemy(Character):
    def __init__(self, pos, groups, player, xp_group):
        super().__init__(groups)
        self.player = player
        self.xp_group = xp_group 
        
        # FIX: Salva explicitamente o grupo de "all_sprites" (que é o primeiro da lista groups)
        # para não correr risco de pegar o grupo errado depois
        self.game_sprites = groups[0] 
        
        original_image = pygame.image.load('assets/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 40))
        self.rect = self.image.get_rect(topleft=pos)
        
        self.speed = 2 
        self.health = 20
        self.xp_value = 10 

    # ... (método chase_player continua igual) ...
    def chase_player(self):
        player_vec = pygame.math.Vector2(self.player.rect.center)
        enemy_vec = pygame.math.Vector2(self.rect.center)
        
        direction_vector = player_vec - enemy_vec
        if direction_vector.magnitude() > 0:
            self.direction = direction_vector.normalize()
        else:
            self.direction = pygame.math.Vector2()

    def die(self):
        # FIX: Usa self.game_sprites em vez de self.groups()[0]
        # Isso garante que o XP vai pro grupo certo e não pro de inimigos
        ExperienceOrb(self.rect.center, [self.game_sprites, self.xp_group], self.xp_value)
        self.kill()

    def update(self):
        self.chase_player()
        self.move(self.speed)