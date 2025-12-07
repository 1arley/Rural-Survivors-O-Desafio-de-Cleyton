import pygame
from settings import *
from src.utils.helpers import AssetManager

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.assets = AssetManager()
        self.font = self.assets.load_font(24)
        
        # Barras
        self.health_bar_rect = pygame.Rect(10, 10, 200, 20)
        self.xp_bar_rect = pygame.Rect(0, HEIGHT - 20, WIDTH, 20)

    def show_bar(self, current, max_val, bg_rect, color):
        pygame.draw.rect(self.display_surface, (50, 50, 50), bg_rect) # Fundo
        
        ratio = current / max_val
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, (255, 255, 255), bg_rect, 2) # Borda

    def show_xp(self, xp, target):
        self.show_bar(xp, target, self.xp_bar_rect, (0, 200, 255))

    def show_timer(self, milliseconds):
        seconds = int(milliseconds / 1000) % 60
        minutes = int(milliseconds / 1000 / 60)
        time_surf = self.font.render(f'{minutes:02d}:{seconds:02d}', True, COLORS['text'])
        time_rect = time_surf.get_rect(center=(WIDTH // 2, 30))
        self.display_surface.blit(time_surf, time_rect)

    def display(self, player, game_time):
        self.show_bar(player.health, player.stats['hp'], self.health_bar_rect, (200, 0, 0))
        self.show_xp(player.xp, player.next_level_xp)
        self.show_timer(game_time)
        
        # Level Text
        lvl_surf = self.font.render(f'Período: {player.level}', True, COLORS['text'])
        self.display_surface.blit(lvl_surf, (10, 40))
        
        # Coins/Créditos
        coin_surf = self.font.render(f'Créditos: {int(player.credits)}', True, (255, 215, 0))
        self.display_surface.blit(coin_surf, (10, 70))