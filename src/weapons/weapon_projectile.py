import pygame
import math
import random
from src.utils.helpers import AssetManager
from src.weapons.weapon import Weapon, AttackSprite

class Projectile(AttackSprite):
    def __init__(self, player, pos, direction, speed, damage, life, groups, image_key, data, scale=1.0):
        super().__init__(groups, damage, 'projectile')
        self.player = player
        self.assets = AssetManager()
        self.data = data
        
        # --- VISUAL & ESCALA ---
        self.original_image = self.assets.get_surface(
            image_key, 
            target_size=None, 
            color_key=image_key, 
            scale_factor=scale
        )
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy()
        
        # --- MOVIMENTO ---
        self.direction = direction
        self.speed = speed
        self.base_speed = speed
        self.current_speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.life = life
        
        # --- MECÂNICAS ESPECIAIS ---
        self.ignored_enemies = []
        
        self.bounces_left = data.get('bounces', 0)
        self.pierce_left = data.get('pierce', 0)
        self.damage_decay = data.get('damage_decay', 0.0)

        # Orbital
        self.is_orbiting = data.get('orbit', False)
        if self.is_orbiting:
            self.angle = 0 # Ângulo de posição (física)
            self.radius = data.get('range', 100)
            self.orbit_speed = speed

        # Persistente
        self.is_persistent = data.get('persistent', False)
        self.tick_timer = 0
        self.tick_rate = 300 

        # Bumerangue
        self.is_boomerang = data.get('boomerang', False)
        self.returning = False
        # Volta quando passar 40% da vida útil
        self.return_time = life * 0.4
        
        # Rotação Visual (Spin)
        self.should_spin = data.get('spin', False)
        self.visual_angle = 0
        self.spin_speed = 20 # Graus por frame

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        time_alive = current_time - self.spawn_time

        # --- LÓGICA DE ROTAÇÃO VISUAL ---
        if self.should_spin:
            self.visual_angle = (self.visual_angle + self.spin_speed) % 360
            self.image = pygame.transform.rotate(self.original_image, self.visual_angle)
            self.rect = self.image.get_rect(center=self.hitbox.center)

        # 1. Movimento Orbital
        if self.is_orbiting:
            self.angle += self.orbit_speed * dt
            ox = self.player.rect.centerx + math.cos(math.radians(self.angle)) * self.radius
            oy = self.player.rect.centery + math.sin(math.radians(self.angle)) * self.radius
            self.rect.center = (ox, oy)
            self.hitbox.center = self.rect.center
            
        # 2. Movimento Bumerangue
        elif self.is_boomerang:
            # Checa se já passou do tempo de ir e deve voltar
            if not self.returning and time_alive >= self.return_time:
                self.returning = True
                # --- CORREÇÃO: Limpa a lista de quem já apanhou para bater neles de novo na volta ---
                self.ignored_enemies = [] 
            
            if self.returning:
                p_pos = pygame.math.Vector2(self.player.rect.center)
                my_pos = pygame.math.Vector2(self.rect.center)
                vec_to_player = p_pos - my_pos
                if vec_to_player.magnitude() > 0:
                    self.direction = vec_to_player.normalize()
            
            self.rect.center += self.direction * self.speed * dt
            self.hitbox.center = self.rect.center
            
            if self.returning and self.rect.colliderect(self.player.hitbox):
                self.kill()

        # 3. Movimento Linear Normal
        else:
            if self.speed > 0:
                self.rect.center += self.direction * self.speed * dt
                self.hitbox.center = self.rect.center

        # 4. Dano Contínuo
        if self.is_persistent:
            if current_time - self.tick_timer > self.tick_rate:
                self.hit_list = [] 
                self.tick_timer = current_time

        # 5. Morte por Tempo
        if not self.is_orbiting:
            if time_alive > self.life:
                self.kill()

class ProjectileWeapon(Weapon):
    def __init__(self, player, groups, data):
        super().__init__(player, groups, data)
        self.orbitals_group = pygame.sprite.Group()

    def activate(self):
        enemies = self.groups['enemy_sprites']
        target_dir = pygame.math.Vector2(1, 0)

        if self.data.get('random_aim'):
            angle = random.uniform(0, 360)
            target_dir = pygame.math.Vector2(1, 0).rotate(angle)
        elif enemies and self.data['speed'] > 0 and not self.data.get('orbit'):
            closest = min([e for e in enemies], 
                          key=lambda e: pygame.math.Vector2(e.rect.center).distance_to(self.player.rect.center))
            p_pos = pygame.math.Vector2(self.player.rect.center)
            e_pos = pygame.math.Vector2(closest.rect.center)
            diff_vector = e_pos - p_pos
            if diff_vector.magnitude() > 0:
                target_dir = diff_vector.normalize()

        final_dmg = self.damage * self.player.modifiers['damage']
        final_speed = self.data['speed'] * self.player.modifiers['proj_speed']
        final_life = self.data['life'] * self.player.modifiers['duration']
        base_scale = self.data.get('scale', 1.0)
        final_scale = base_scale * self.player.modifiers['area']
        amount = 1 + int(self.player.modifiers['amount'])
        is_orbit = self.data.get('orbit', False)
        
        if is_orbit:
            if len(self.orbitals_group) == amount:
                for sprite in self.orbitals_group:
                    sprite.damage = final_dmg
                    sprite.orbit_speed = final_speed
                return
            else:
                for sprite in self.orbitals_group:
                    sprite.kill()
                for i in range(amount):
                    proj = Projectile(
                        self.player, self.player.rect.center, target_dir, final_speed, final_dmg, final_life, 
                        [self.groups['all_sprites'], self.groups['attack_sprites']],
                        self.data.get('image', 'proj'), self.data, scale=final_scale
                    )
                    proj.angle = (360 / amount) * i
                    self.orbitals_group.add(proj)
                return

        for i in range(amount):
            current_dir = target_dir
            if amount > 1 and not self.data.get('random_aim'):
                angle_offset = (i - (amount - 1) / 2) * 15
                current_dir = target_dir.rotate(angle_offset)
            
            if self.data.get('random_aim') and amount > 1:
                 angle = random.uniform(0, 360)
                 current_dir = pygame.math.Vector2(1, 0).rotate(angle)

            Projectile(
                self.player, self.player.rect.center, current_dir, final_speed, final_dmg, final_life, 
                [self.groups['all_sprites'], self.groups['attack_sprites']],
                self.data.get('image', 'proj'), self.data, scale=final_scale
            )