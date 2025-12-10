import pygame
from settings import *
from src.utils.helpers import AssetManager

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.assets = AssetManager()
        self.font = self.assets.load_font(24)
        self.small_font = self.assets.load_font(18)
        
        # Barras
        self.health_bar_rect = pygame.Rect(10, 10, 200, 20)
        self.xp_bar_rect = pygame.Rect(0, HEIGHT - 20, WIDTH, 20)

    def show_bar(self, current, max_val, bg_rect, color):
        pygame.draw.rect(self.display_surface, (50, 50, 50), bg_rect)
        
        ratio = current / max_val
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, (255, 255, 255), bg_rect, 2)

    def show_xp(self, xp, target):
        self.show_bar(xp, target, self.xp_bar_rect, (0, 200, 255))

    def show_timer(self, milliseconds):
        seconds = int(milliseconds / 1000) % 60
        minutes = int(milliseconds / 1000 / 60)
        time_surf = self.font.render(f'{minutes:02d}:{seconds:02d}', True, COLORS['text'])
        time_rect = time_surf.get_rect(center=(WIDTH // 2, 30))
        self.display_surface.blit(time_surf, time_rect)

    def draw_inventory(self, player):
        # Configuração dos quadrados
        slot_size = 40
        padding = 5
        start_x = WIDTH - (4 * (slot_size + padding)) - 10
        start_y = 10
        
        # --- DESENHAR ARMAS (Linha 1) ---
        weapons = player.weapon_controller.weapons if player.weapon_controller else []
        for i in range(4):
            x = start_x + i * (slot_size + padding)
            y = start_y
            rect = pygame.Rect(x, y, slot_size, slot_size)
            
            # Fundo
            pygame.draw.rect(self.display_surface, (0, 0, 0, 150), rect)
            pygame.draw.rect(self.display_surface, (100, 100, 100), rect, 2)
            
            if i < len(weapons):
                w = weapons[i]
                # Ícone
                icon_key = f"icon_{w.key}"
                icon = self.assets.get_surface(icon_key, (slot_size-4, slot_size-4), 'white')
                self.display_surface.blit(icon, (x+2, y+2))
                
                # Nível (Pequeno texto no canto)
                lvl_surf = self.small_font.render(str(w.lvl), True, (255, 255, 255))
                self.display_surface.blit(lvl_surf, (x + 2, y + slot_size - 15))

        # --- DESENHAR PASSIVOS (Linha 2) ---
        passives = player.passives
        for i in range(4):
            x = start_x + i * (slot_size + padding)
            y = start_y + slot_size + padding
            rect = pygame.Rect(x, y, slot_size, slot_size)
            
            pygame.draw.rect(self.display_surface, (0, 0, 0, 150), rect)
            pygame.draw.rect(self.display_surface, (100, 100, 100), rect, 2)
            
            if i < len(passives):
                p = passives[i]
                icon_key = f"icon_{p['key']}"
                icon = self.assets.get_surface(icon_key, (slot_size-4, slot_size-4), 'white')
                self.display_surface.blit(icon, (x+2, y+2))
                
                lvl_surf = self.small_font.render(str(p['level']), True, (255, 255, 0))
                self.display_surface.blit(lvl_surf, (x + 2, y + slot_size - 15))

    def display(self, player, game_time):
        self.show_bar(player.health, player.stats['hp'], self.health_bar_rect, (200, 0, 0))
        self.show_xp(player.xp, player.next_level_xp)
        self.show_timer(game_time)
        self.draw_inventory(player) # Chama a nova função
        
        # Texto de Nível e Créditos
        lvl_surf = self.font.render(f'Nível: {player.level}', True, COLORS['text'])
        self.display_surface.blit(lvl_surf, (10, 40))
        
        coin_surf = self.font.render(f'Créditos: {int(player.credits)}', True, (255, 215, 0))
        self.display_surface.blit(coin_surf, (10, 70))