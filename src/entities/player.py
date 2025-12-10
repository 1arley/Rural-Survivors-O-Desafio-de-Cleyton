import pygame
from math import sin
from .entity import Entity
from settings import *
from src.utils.helpers import AssetManager
from src.ui.damage_text import DamageText
from src.systems.save_manager import SaveManager

class Player(Entity):
    def __init__(self, pos, groups, obstacles_sprites, create_attack, destroy_attack, char_data):
        super().__init__(groups)
        self.assets = AssetManager()
        
        self.image = self.assets.get_surface(
            key=char_data['color'], 
            color_key=char_data['color'] 
        )
        
        self.rect = self.image.get_rect(topleft=pos)
        self.set_hitbox()
        
        self.visual_groups = groups 
        
        self.stats = {
            'hp': char_data['hp'], 
            'speed': char_data['speed'], 
            'attack': 10
        }
        self.health = self.stats['hp']
        
        self.modifiers = {
            'damage': 1.0, 'speed': 1.0, 'xp_mult': 1.0, 'armor': 0, 
            'area': 1.0, 'cooldown': 1.0, 'proj_speed': 1.0, 'duration': 1.0, 
            'amount': 0, 'luck': 0, 'regen': 0, 'magnet': 1.0, 'evasion': 0,
            'knockback': 0, 'gold_gain': 1.0,
            'crit_chance': 5, 'crit_mult': 1.5
        }
        
        self.apply_permanent_upgrades()

        self.invulnerable = False
        self.hurt_time = 0
        self.invulnerability_duration = 500
        
        self.xp = 0
        self.level = 1
        self.next_level_xp = 10
        self.credits = 0 
        self.kill_count = 0 # NOVO: Contador de Kills
        
        self.base_magnet_radius = char_data['magnet']
        self.magnet_radius = self.base_magnet_radius
        
        self.weapons = [] 
        self.passives = [] 
        self.inventory = {} 
        
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = 0
        self.create_attack = create_attack 
        self.weapon_controller = None

    def apply_permanent_upgrades(self):
        save_data = SaveManager().data['upgrades']
        self.stats['hp'] += save_data.get('max_hp', 0) * 10
        self.health = self.stats['hp']
        self.modifiers['damage'] += save_data.get('damage', 0) * 0.05
        self.modifiers['speed'] += save_data.get('speed', 0) * 0.05
        self.modifiers['xp_mult'] += save_data.get('xp_gain', 0) * 0.1
        self.modifiers['gold_gain'] += save_data.get('gold_gain', 0) * 0.1

    def apply_passive(self, passive_key, passive_data):
        if passive_key in self.inventory:
            self.inventory[passive_key] += 1
            for p in self.passives:
                if p['key'] == passive_key:
                    p['level'] += 1
                    break
        else:
            self.inventory[passive_key] = 1
            new_passive = passive_data.copy()
            new_passive['key'] = passive_key
            new_passive['level'] = 1
            self.passives.append(new_passive)
            
        stat = passive_data['stat']
        val = passive_data['value']
        
        if stat in self.modifiers:
            if stat in ['max_hp', 'hp']:
                if stat == 'max_hp':
                    self.stats['hp'] += val
                    self.health += val
            elif stat in ['armor', 'amount', 'luck', 'regen', 'evasion', 'knockback', 'crit_chance']:
                self.modifiers[stat] += val
            else:
                self.modifiers[stat] += val
                
        if stat == 'magnet':
            self.magnet_radius = self.base_magnet_radius * self.modifiers['magnet']
        
        print(f"Passivo {passive_data['name']} (Lv {self.inventory[passive_key]}) aplicado!")

    def input(self):
        keys = pygame.key.get_pressed()
        up_pressed = keys[pygame.K_w] or keys[pygame.K_UP]
        down_pressed = keys[pygame.K_s] or keys[pygame.K_DOWN]
        right_pressed = keys[pygame.K_d] or keys[pygame.K_RIGHT]
        left_pressed = keys[pygame.K_a] or keys[pygame.K_LEFT]

        self.direction.y = int(down_pressed) - int(up_pressed)
        self.direction.x = int(right_pressed) - int(left_pressed)

    def get_xp(self, amount):
        self.xp += amount * self.modifiers['xp_mult']

    def level_up(self):
        self.xp -= self.next_level_xp
        self.level += 1
        self.next_level_xp = int(self.next_level_xp * 1.2)

    def take_damage(self, amount):
        if not self.invulnerable:
            import random
            if self.modifiers['evasion'] > 0 and random.randint(0, 100) < self.modifiers['evasion']:
                DamageText(self.rect.midtop, "ESQUIVA!", self.visual_groups)
                return 

            final_damage = max(1, amount - self.modifiers['armor'])
            self.health -= final_damage
            self.invulnerable = True
            self.hurt_time = pygame.time.get_ticks()

    def invulnerability_timer(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.invulnerable = False
                self.image.set_alpha(255)

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0: return 255
        else: return 0

    def regen_health(self, dt):
        if self.modifiers['regen'] > 0 and self.health < self.stats['hp']:
            self.health += self.modifiers['regen'] * dt
            if self.health > self.stats['hp']:
                self.health = self.stats['hp']

    def update(self, dt):
        self.input()
        current_speed = self.stats['speed'] * self.modifiers['speed']
        self.move(current_speed * dt)
        self.invulnerability_timer()
        self.regen_health(dt)