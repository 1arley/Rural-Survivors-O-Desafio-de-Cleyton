import pygame
from settings import *

class Menu:
    def __init__(self, font):
        self.display_surface = pygame.display.get_surface()
        self.font = font

    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x, y))
        self.display_surface.blit(text_surf, text_rect)

class CharacterSelectMenu(Menu):
    def __init__(self, font, chars_data):
        super().__init__(font)
        self.chars_data = chars_data
        self.options = ['calouro', 'veterano']
        self.selected_index = 0

    def draw(self):
        self.display_surface.fill(COLORS['bg'])
        self.draw_text("SELECIONE SEU PERSONAGEM", 50, WIDTH//2, 100, (255, 215, 0))

        # Desenha opções
        for index, char_key in enumerate(self.options):
            data = self.chars_data[char_key]
            color = (255, 255, 255) if index == self.selected_index else (100, 100, 100)
            
            x_pos = WIDTH//4 if index == 0 else 3*WIDTH//4
            
            # Caixa de Seleção
            pygame.draw.rect(self.display_surface, color, (x_pos - 150, 200, 300, 400), 2)
            
            self.draw_text(data['name'].upper(), 40, x_pos, 250, color)
            self.draw_text(f"HP: {data['hp']}", 30, x_pos, 320)
            self.draw_text(f"Speed: {data['speed']}", 30, x_pos, 360)
            self.draw_text(data['desc'], 20, x_pos, 450)

        self.draw_text("[SETAS] Mover   [ENTER] Selecionar", 30, WIDTH//2, HEIGHT - 50)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.selected_index = 0
                if event.key == pygame.K_RIGHT:
                    self.selected_index = 1
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.options[self.selected_index]
        return None

class LevelUpMenu(Menu):
    def __init__(self, font):
        super().__init__(font)
        self.options = [] # Lista de dicionários {'type': 'weapon'/'passive', 'key': 'name', ...}

    def set_options(self, options):
        self.options = options

    def draw(self):
        # Overlay escuro
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.display_surface.blit(overlay, (0,0))
        
        self.draw_text("LEVEL UP!", 60, WIDTH//2, 100, (255, 215, 0))
        self.draw_text("Escolha uma melhoria:", 40, WIDTH//2, 160)

        start_y = 250
        for i, opt in enumerate(self.options):
            color = (255, 255, 255)
            # Destaque baseado na raridade ou tipo poderia ser aqui
            
            text = f"{i+1}. {opt['display_name']} (Lvl {opt['lvl']} -> {opt['lvl']+1})"
            desc = opt['desc']
            
            pygame.draw.rect(self.display_surface, (50, 50, 50), (WIDTH//2 - 300, start_y - 20, 600, 80))
            pygame.draw.rect(self.display_surface, (255, 255, 255), (WIDTH//2 - 300, start_y - 20, 600, 80), 2)
            
            self.draw_text(text, 35, WIDTH//2, start_y, (100, 255, 100))
            self.draw_text(desc, 25, WIDTH//2, start_y + 35, (200, 200, 200))
            
            start_y += 100