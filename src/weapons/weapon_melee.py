import pygame
from src.utils.helpers import AssetManager
from src.weapons.weapon import Weapon, AttackSprite

class MeleeSprite(AttackSprite):
    def __init__(self, player, damage, life, area_scale, groups, image_key):
        super().__init__(groups, damage, 'melee')
        self.player = player
        self.assets = AssetManager()
        
        # Tamanho base esticado pelo area_scale
        base_size = (int(100 * area_scale), int(20 * area_scale))
        self.image = self.assets.get_surface(image_key, base_size, 'area_giz', 'rect')
        
        # Posiciona ao lado do player (offset também escala para não ficar dentro do boneco)
        self.offset = pygame.math.Vector2(50 * area_scale, 0)
        
        if player.direction.x < 0:
            self.offset.x *= -1
            self.image = pygame.transform.flip(self.image, True, False)
            
        self.rect = self.image.get_rect(center = player.rect.center + self.offset)
        self.hitbox = self.rect.copy()
        
        self.spawn_time = pygame.time.get_ticks()
        self.life = life

    def update(self, dt):
        self.rect.center = self.player.rect.center + self.offset
        self.hitbox.center = self.rect.center
        if pygame.time.get_ticks() - self.spawn_time > self.life:
            self.kill()

class MeleeWeapon(Weapon):
    def activate(self):
        final_dmg = self.damage * self.player.modifiers['damage']
        
        # --- APLICAÇÃO DE ÁREA ---
        # Base da arma * Modificador do Player
        area = self.data.get('area', 1.0) * self.player.modifiers['area']
        
        # --- CORREÇÃO DO AMOUNT ---
        # Adiciona suporte a quantidade (ex: +1 projetil) para armas melee.
        # Isso cria multiplas instancias do ataque, causando dano múltiplo.
        amount = 1 + int(self.player.modifiers['amount'])
        
        for i in range(amount):
            # Pequeno offset visual se houver mais de um, para não ficarem 100% sobrepostos
            # (Opcional, mas ajuda a ver que o upgrade funcionou)
            # Neste caso, apenas instanciamos. O sistema de colisão do main.py 
            # trata sprites diferentes como hits diferentes.
            
            MeleeSprite(
                self.player, final_dmg, self.data['life'], area,
                [self.groups['all_sprites'], self.groups['attack_sprites']],
                self.data.get('image', 'area_giz')
            )