import pygame
from settings import *
from entity import Character
from projectile import Projectile

class Player(Character):
    def __init__(self, pos, groups, enemy_group, xp_group):
        super().__init__(groups)
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48)) 
        self.rect = self.image.get_rect(topleft=pos)
        
        # Stats de Sobrevivência
        self.speed = 5
        self.health = 100
        self.max_health = 100
        
        # Stats de RPG
        self.xp = 0
        self.level = 1
        self.next_level_xp = 100
        
        # Combate
        self.enemy_group = enemy_group
        self.xp_group = xp_group
        self.can_shoot = True
        self.shoot_timer = 0
        self.shoot_cooldown = 1000 # 1 segundo entre tiros

        # Invencibilidade
        self.can_take_damage = True
        self.hurt_time = 0
        self.invulnerability_duration = 500
    
    def take_damage(self, amount):
        # Só toma dano se não estiver invencível
        if self.can_take_damage:
            # Chama o take_damage original da classe pai (entity.py) pra descontar a vida
            super().take_damage(amount)
            
            # Ativa a invencibilidade
            self.can_take_damage = False
            self.hurt_time = pygame.time.get_ticks()
            
            # Feedback visual: deixa o boneco meio transparente
            self.image.set_alpha(128)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]: self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]: self.direction.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.direction.x = 1

    def level_up(self):
        self.level += 1
        self.xp -= self.next_level_xp
        self.next_level_xp = int(self.next_level_xp * 1.2) # Fica 20% mais difícil upar
        self.shoot_cooldown = max(200, self.shoot_cooldown - 50) # Atira mais rápido
        self.max_health += 20
        self.health = self.max_health # Cura ao upar
        print(f"LEVEL UP! Nível {self.level}")

    def collect_xp(self):
        # Verifica colisão com itens de XP
        collided_xp = pygame.sprite.spritecollide(self, self.xp_group, True)
        for orb in collided_xp:
            self.xp += orb.value
            if self.xp >= self.next_level_xp:
                self.level_up()

    def auto_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_timer >= self.shoot_cooldown:
            if len(self.enemy_group) > 0: # Só atira se tiver inimigo
                Projectile(self.rect.center, [self.groups()[0]], self.enemy_group)
                self.shoot_timer = current_time

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_take_damage:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.can_take_damage = True
                self.image.set_alpha(255)

    def draw_ui(self, surface):
        # Barra de Vida
        bar_width = 60
        bar_height = 10
        x = self.rect.centerx - bar_width // 2
        y = self.rect.bottom + 10
        pygame.draw.rect(surface, BLACK, (x, y, bar_width, bar_height))
        ratio = max(0, self.health) / self.max_health
        pygame.draw.rect(surface, RED, (x, y, bar_width * ratio, bar_height))
        
        # Barra de XP (Azul embaixo da vida)
        xp_ratio = self.xp / self.next_level_xp
        pygame.draw.rect(surface, BLACK, (x, y + 12, bar_width, 5))
        pygame.draw.rect(surface, BLUE, (x, y + 12, bar_width * xp_ratio, 5))

    def update(self):
        self.input()
        self.cooldowns()
        self.auto_shoot()
        self.collect_xp()
        self.move(self.speed)