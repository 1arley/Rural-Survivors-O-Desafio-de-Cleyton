import pygame
import random
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        # Background
        from src.utils.helpers import AssetManager
        self.assets = AssetManager()
        self.floor_surf = self.assets.get_surface('bg_campus', (WIDTH * 2, HEIGHT * 2), 'bg')
        
        if 'assets/environment/campus_floor.png' not in ASSET_PATHS:
             # Fallback Grid
            for x in range(0, WIDTH * 2, TILE_SIZE):
                pygame.draw.line(self.floor_surf, COLORS['grid'], (x, 0), (x, HEIGHT * 2))
            for y in range(0, HEIGHT * 2, TILE_SIZE):
                pygame.draw.line(self.floor_surf, COLORS['grid'], (0, y), (WIDTH * 2, y))
                
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
        
        # --- SCREEN SHAKE ---
        self.shake_duration = 0
        self.shake_intensity = 0

    def shake(self, intensity, duration):
        self.shake_intensity = intensity
        self.shake_duration = duration

    def custom_draw(self, player):
        # 1. Calcula Offset Base
        target_x = player.rect.centerx - self.half_width
        target_y = player.rect.centery - self.half_height
        
        # 2. Aplica Screen Shake
        if self.shake_duration > 0:
            self.shake_duration -= 1
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            target_x += offset_x
            target_y += offset_y
            
        self.offset.x = target_x
        self.offset.y = target_y

        # 3. Desenha Chão
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # 4. Desenha Sprites (Y-Sort)
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
            # Barra de Vida
            if sprite == player:
                bar_width = sprite.rect.width
                bar_height = 5
                bar_x = offset_pos.x
                bar_y = offset_pos.y + sprite.rect.height + 5
                
                ratio = player.health / player.stats['hp']
                current_bar_width = bar_width * ratio
                
                bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                pygame.draw.rect(self.display_surface, (0, 0, 0), bg_rect)
                
                if current_bar_width > 0:
                    health_rect = pygame.Rect(bar_x, bar_y, current_bar_width, bar_height)
                    pygame.draw.rect(self.display_surface, (255, 0, 0), health_rect)