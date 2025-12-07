import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # Configuração do Offset (deslocamento)
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        
        # Setup do Chão (Grid Infinito)
        self.floor_surf = pygame.Surface((WIDTH * 2, HEIGHT * 2)) # Tamanho arbitrário para textura
        self.floor_surf.fill(COLORS['bg'])
        # Desenha o grid no chão uma vez
        for x in range(0, WIDTH * 2, TILE_SIZE):
            pygame.draw.line(self.floor_surf, COLORS['grid'], (x, 0), (x, HEIGHT * 2))
        for y in range(0, HEIGHT * 2, TILE_SIZE):
            pygame.draw.line(self.floor_surf, COLORS['grid'], (0, y), (WIDTH * 2, y))
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self, player):
        # 1. Calcular o offset baseado na posição do player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # 2. Desenhar o Chão (com offset)
        # Para efeito infinito simples, movemos o rect do chão oposto ao player
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # 3. Desenhar Sprites com Y-Sort (profundidade)
        # Ordena sprites pela base (centery) para dar ilusão de 3D
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
            # (Opcional) Debug: Desenhar retângulos de colisão
            # pygame.draw.rect(self.display_surface, (255,0,0), sprite.hitbox.move(-self.offset.x, -self.offset.y), 1)