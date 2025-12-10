import pygame
from .entity import Entity
from settings import *
from src.utils.helpers import AssetManager
from src.ui.damage_text import DamageText 

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, player, stats, is_elite=False):
        super().__init__(groups)
        self.player = player
        self.assets = AssetManager()
        self.stats = stats 
        
        self.is_elite = is_elite
        self.is_boss = stats.get('is_boss', False)
        
        type_mapping = {
            'lista_exercicio': 'enemy_basic', 'prazo_curto': 'enemy_basic',
            'gato_campus': 'enemy_fast', 'trabalho_grupo': 'enemy_fast',
            'onibus_lotado': 'enemy_tank', 'prova_final': 'enemy_tank',
            'ead': 'enemy_ranged', 'seminario': 'enemy_elite',
            'banca': 'enemy_boss', 'coordenador': 'enemy_boss', 'reitoria': 'enemy_boss', 'tcc': 'enemy_boss'
        }
        self.color_key = type_mapping.get(monster_name, 'enemy_basic')
        
        base_scale = stats.get('scale', 1.0)
        if self.is_elite and not self.is_boss:
            base_scale *= 1.3 
            
        size = int(40 * base_scale)
        self.original_image = self.assets.get_surface(monster_name, (size, size), self.color_key, 'rect')
        self.image = self.original_image.copy()
        
        self.rect = self.image.get_rect(topleft=pos)
        self.set_hitbox()
        
        # Elite Stats Boost
        multiplier = 2.0 if self.is_elite else 1.0
        
        self.base_speed = stats['speed'] * (1.1 if self.is_elite else 1.0)
        self.speed = self.base_speed
        self.health = stats['hp'] * multiplier
        self.damage = stats['damage'] * (1.5 if self.is_elite else 1.0)
        self.xp_value = stats['xp'] * (3 if self.is_elite else 1)
        
        self.behavior = stats.get('behavior', 'chase')
        self.attack_range = stats.get('attack_range', 0)
        self.attack_cooldown = stats.get('attack_cooldown', 0)
        self.last_attack_time = 0
        
        self.status_effects = {'slow': {'factor': 1.0, 'end_time': 0}, 'burn': {'damage': 0, 'next_tick': 0, 'end_time': 0}}
        self.knockback_direction = pygame.math.Vector2()
        self.knockback_duration = 0
        self.knockback_speed = 0
        self.flash_duration = 0 
        self.projectile_groups = None 

    def get_player_distance_direction(self):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(self.player.rect.center)
        diff = player_vec - enemy_vec
        distance = diff.magnitude()
        direction = diff.normalize() if distance > 0 else pygame.math.Vector2()
        return (distance, direction)

    def apply_slow(self, factor, duration):
        self.status_effects['slow']['factor'] = factor
        self.status_effects['slow']['end_time'] = pygame.time.get_ticks() + duration

    def apply_burn(self, damage, duration):
        now = pygame.time.get_ticks()
        current = self.status_effects['burn']
        if now > current['end_time'] or damage >= current['damage']:
            current['damage'] = damage
            current['end_time'] = now + duration
            if now > current['end_time']: current['next_tick'] = now

    def apply_knockback(self, direction, force):
        self.knockback_direction = direction.normalize()
        self.knockback_speed = force * 100
        self.knockback_duration = 100

    def trigger_flash(self):
        self.flash_duration = 5 

    def update_status_visuals(self, current_time):
        """Aplica efeitos visuais sobre a imagem ATUAL (que já foi animada)"""
        is_burning = False
        
        # Lógica de Status (Dano)
        if current_time > self.status_effects['slow']['end_time']:
            self.status_effects['slow']['factor'] = 1.0
        self.speed = self.base_speed * self.status_effects['slow']['factor']
        
        burn = self.status_effects['burn']
        if current_time < burn['end_time']:
            is_burning = True
            if current_time >= burn['next_tick']:
                dmg = burn['damage']
                self.health -= dmg
                self.trigger_flash()
                burn['next_tick'] = current_time + 500
                if hasattr(self.player, 'visual_groups'):
                    DamageText(self.rect.midtop, str(dmg), self.player.visual_groups)
        
        # --- DESENHO DOS EFEITOS (EM ORDEM) ---
        
        # 1. Tintura de Fogo
        if is_burning:
            tint_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint_surf.fill((255, 50, 0, 100))
            self.image.blit(tint_surf, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
            
        # 2. Flash de Dano (Branco)
        if self.flash_duration > 0:
            self.flash_duration -= 1
            flash_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, 200))
            self.image.blit(flash_surf, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

        # 3. Coroa de Elite (SEMPRE POR CIMA DE TUDO)
        if self.is_elite and not self.is_boss:
            center_x = self.rect.width // 2
            # Desenha borda preta para destacar
            pygame.draw.circle(self.image, (0,0,0), (center_x, 8), 7) 
            # Desenha o ouro
            pygame.draw.circle(self.image, COLORS['elite_crown'], (center_x, 8), 5)

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        
        # --- CORREÇÃO DE ORDEM ---
        # 1. Anima primeiro (define a forma base do sprite)
        self.animate(dt)
        
        # 2. Cria cópia para não "sujar" o original da animação com tintas
        self.image = self.image.copy()
        
        # 3. Aplica efeitos visuais e lógicos na cópia
        self.update_status_visuals(current_time)
        
        if self.health <= 0:
            self.kill()
            return

        if self.knockback_duration > 0:
            self.knockback_duration -= dt * 1000
            self.move(self.knockback_speed * dt)
            self.knockback_speed = max(0, self.knockback_speed * 0.8)
            return

        dist, direction = self.get_player_distance_direction()
        self.direction = direction
        
        if self.behavior == 'ranged':
            if dist > self.attack_range:
                self.move(self.speed * dt)
            else:
                if current_time - self.last_attack_time >= self.attack_cooldown:
                    self.shoot(direction)
                    self.last_attack_time = current_time
        else:
            self.move(self.speed * dt)

    def shoot(self, direction):
        from src.entities.enemy_projectile import EnemyProjectile
        if self.projectile_groups:
            EnemyProjectile(self.rect.center, direction, 300, self.damage, self.projectile_groups)