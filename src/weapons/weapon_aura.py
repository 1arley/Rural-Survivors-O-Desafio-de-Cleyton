import pygame
from src.utils.helpers import AssetManager
from src.weapons.weapon import Weapon, AttackSprite

class AuraSprite(AttackSprite):
    def __init__(self, player, damage, area_scale, groups, image_key, data):
        super().__init__(groups, damage, 'aura')
        self.player = player
        self.assets = AssetManager()
        self.data = data # Guarda os dados (incluindo 'slow') para usar na colisão
        
        size = int(120 * area_scale)
        self.image = self.assets.get_surface(image_key, (size, size), 'area_giz', 'circle')
        self.image.set_alpha(100)
        
        self.rect = self.image.get_rect(center=player.rect.center)
        self.hitbox = self.rect.inflate(-20, -20)

    def update(self, dt):
        self.rect.center = self.player.rect.center
        self.hitbox.center = self.rect.center

class AuraWeapon(Weapon):
    def __init__(self, player, groups, data):
        super().__init__(player, groups, data)
        self.sprite = None
        self.current_area_mod = 0 

    def activate(self):
        final_dmg = self.damage * self.player.modifiers['damage']
        player_area_mod = self.player.modifiers['area']
        
        if self.sprite and self.sprite.alive():
            if self.current_area_mod != player_area_mod:
                self.sprite.kill() 
        
        if not self.sprite or not self.sprite.alive():
            area = self.data.get('area', 1.0) * player_area_mod
            self.sprite = AuraSprite(
                self.player, final_dmg, area,
                [self.groups['all_sprites'], self.groups['attack_sprites']],
                self.data.get('image', 'area_giz'),
                self.data # Passa os dados brutos da arma (JSON)
            )
            self.current_area_mod = player_area_mod
        else:
            self.sprite.damage = final_dmg
        
        if self.sprite:
            self.sprite.hit_list = []