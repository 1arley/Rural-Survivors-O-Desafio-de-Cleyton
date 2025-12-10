import pygame
from settings import *
from src.utils.helpers import AssetManager
from src.systems.save_manager import SaveManager

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
        self.options = ['calouro', 'veterano', 'monitor', 'pesquisador']
        self.selected_index = 0
        self.assets = AssetManager()

    def draw(self):
        self.display_surface.fill(COLORS['bg'])
        self.draw_text("SELECIONE SEU PERSONAGEM", 50, WIDTH//2, 80, (255, 215, 0))
        
        char_key = self.options[self.selected_index]
        data = self.chars_data[char_key]
        cx, cy = WIDTH // 2, HEIGHT // 2
        
        self.draw_text("<", 80, cx - 300, cy, (255, 255, 0))
        self.draw_text(">", 80, cx + 300, cy, (255, 255, 0))

        card_rect = pygame.Rect(0, 0, 400, 450)
        card_rect.center = (cx, cy)
        pygame.draw.rect(self.display_surface, (40, 40, 50), card_rect)
        pygame.draw.rect(self.display_surface, (255, 255, 255), card_rect, 3)
        
        char_img = self.assets.get_surface(data['color'], (100, 100), data['color'])
        img_rect = char_img.get_rect(center=(cx, cy - 100))
        self.display_surface.blit(char_img, img_rect)

        self.draw_text(data['name'].upper(), 50, cx, cy - 200, (255, 255, 255))
        self.draw_text(f"Vida: {data['hp']}", 30, cx, cy, (255, 100, 100))
        self.draw_text(f"Velocidade: {data['speed']}", 30, cx, cy + 40, (100, 255, 100))
        self.draw_text(f"Coleta: {data['magnet']}", 30, cx, cy + 80, (100, 200, 255))
        self.draw_text(data['desc'], 25, cx, cy + 150, (200, 200, 200))
        self.draw_text("SETAS | ENTER", 25, cx, HEIGHT - 50, (150, 150, 150))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    return self.options[self.selected_index]
                if event.key == pygame.K_ESCAPE: return 'back'
        return None

class MainMenu(Menu):
    def __init__(self, font):
        super().__init__(font)
        self.options = ['JOGAR', 'SECRETARIA', 'SAIR']
        self.selected_index = 0
        self.assets = AssetManager()
        self.bg_image = self.assets.get_surface('title_screen', target_size=(WIDTH, HEIGHT), color_key='menu_bg')

    def draw(self):
        self.display_surface.blit(self.bg_image, (0, 0))
        self.draw_text(TITLE, 60, WIDTH//2, HEIGHT//4, COLORS.get('title_text', (255, 255, 0)))
        for index, option in enumerate(self.options):
            color = COLORS['selected_option'] if index == self.selected_index else COLORS['unselected_option']
            y_pos = HEIGHT//2 + index * 60
            text = f"> {option} <" if index == self.selected_index else option
            self.draw_text(text, 40, WIDTH//2, y_pos, color)
        self.draw_text("WASD/SETAS e ENTER/ESPAÇO", 20, WIDTH//2, HEIGHT - 40, (150, 150, 150))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    if self.selected_index == 0: return 'play'
                    elif self.selected_index == 1: return 'shop'
                    else: return 'quit'
        return None

class ShopMenu(Menu):
    def __init__(self, font):
        super().__init__(font)
        self.save_manager = SaveManager()
        self.options = list(self.save_manager.upgrades_info.keys())
        self.selected_index = 0
        self.message = ""
        self.message_timer = 0

    def draw(self):
        self.display_surface.fill(COLORS['menu_bg'])
        
        self.draw_text("SECRETARIA ACADÊMICA", 50, WIDTH//2, 50, (255, 215, 0))
        self.draw_text(f"Seus Créditos: {self.save_manager.data['credits']}", 40, WIDTH//2, 100, (100, 255, 100))

        start_y = 160
        for index, key in enumerate(self.options):
            info = self.save_manager.upgrades_info[key]
            current_lvl = self.save_manager.data['upgrades'][key]
            cost = self.save_manager.get_upgrade_cost(key)
            
            color = (255, 255, 255)
            if index == self.selected_index: color = (255, 255, 0)
            
            text_name = f"{info['name']} (Nv. {current_lvl})"
            text_desc = info['desc']
            text_cost = f"{cost} C"
            
            y = start_y + index * 80
            if index == self.selected_index:
                self.draw_text(">", 40, WIDTH//2 - 400, y, (255, 255, 0))
            
            self.draw_text(text_name, 35, WIDTH//2 - 200, y, color)
            
            # --- CORREÇÃO AQUI: ADICIONADO O ARGUMENTO 'y' ---
            self.draw_text(text_cost, 35, WIDTH//2 + 200, y, (255, 100, 100) if self.save_manager.data['credits'] < cost else (100, 255, 100))
            
            self.draw_text(text_desc, 20, WIDTH//2, y + 30, (150, 150, 150))

        if pygame.time.get_ticks() < self.message_timer:
            self.draw_text(self.message, 30, WIDTH//2, HEIGHT - 100, (255, 255, 255))

        self.draw_text("[ESC] Voltar   [ENTER] Comprar", 25, WIDTH//2, HEIGHT - 40, (150, 150, 150))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'back'
                
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    key = self.options[self.selected_index]
                    success = self.save_manager.buy_upgrade(key)
                    if success:
                        self.message = "Matrícula realizada!"
                    else:
                        self.message = "Créditos insuficientes!"
                    self.message_timer = pygame.time.get_ticks() + 2000
        return None

class PauseMenu(Menu):
    def __init__(self, font, game=None):
        super().__init__(font)
        self.game = game
        self.options = ['CONTINUAR', 'MENU PRINCIPAL', 'SAIR DO JOGO']
        self.selected_index = 0
        self.assets = AssetManager()

    def draw(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.display_surface.blit(overlay, (0,0))
        
        self.draw_text("JOGO PAUSADO", 60, WIDTH//2, 100, (255, 215, 0))

        if self.game and self.game.player:
            p = self.game.player
            stats_x = WIDTH - 300
            stats_y = 150
            
            pygame.draw.rect(self.display_surface, (30, 30, 40), (stats_x - 20, stats_y - 20, 250, 400))
            pygame.draw.rect(self.display_surface, (200, 200, 200), (stats_x - 20, stats_y - 20, 250, 400), 2)
            
            self.draw_text("ESTATÍSTICAS", 30, stats_x + 100, stats_y, (255, 255, 0))
            
            mods = p.modifiers
            lines = [
                f"Vida Máx: {int(p.stats['hp'])}",
                f"Dano: x{mods['damage']:.2f}",
                f"Velocidade: x{mods['speed']:.2f}",
                f"Área: x{mods['area']:.2f}",
                f"Cooldown: x{mods['cooldown']:.2f}",
                f"Proj. Speed: x{mods['proj_speed']:.2f}",
                f"Duração: x{mods['duration']:.2f}",
                f"Qtd. Extra: +{mods['amount']}",
                f"Armadura: {mods['armor']}",
                f"Regen: {mods['regen']}/s",
                f"XP Bonus: x{mods['xp_mult']:.2f}",
            ]
            
            font_small = self.assets.load_font(22)
            for i, line in enumerate(lines):
                surf = font_small.render(line, True, (255, 255, 255))
                self.display_surface.blit(surf, (stats_x, stats_y + 40 + i * 30))

        for index, option in enumerate(self.options):
            color = COLORS['selected_option'] if index == self.selected_index else COLORS['unselected_option']
            y_pos = HEIGHT//2 + index * 60
            text = f"> {option} <" if index == self.selected_index else option
            self.draw_text(text, 40, WIDTH//3, y_pos, color)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit_game'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return 'resume'
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    if self.selected_index == 0: return 'resume'
                    elif self.selected_index == 1: return 'main_menu'
                    elif self.selected_index == 2: return 'quit_game'
        return None

class LevelUpMenu(Menu):
    def __init__(self, font):
        super().__init__(font)
        self.options = []
        self.assets = AssetManager()

    def set_options(self, options):
        self.options = options

    def draw(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.display_surface.blit(overlay, (0,0))
        
        self.draw_text("LEVEL UP!", 60, WIDTH//2, 80, (255, 215, 0))
        self.draw_text("Escolha uma melhoria (1, 2, 3):", 30, WIDTH//2, 130)

        start_y = 200
        for i, opt in enumerate(self.options):
            rect_bg = pygame.Rect(WIDTH//2 - 300, start_y, 600, 100)
            pygame.draw.rect(self.display_surface, (50, 50, 50), rect_bg)
            pygame.draw.rect(self.display_surface, (255, 255, 255), rect_bg, 2)
            
            if opt['type'] == 'weapon':
                icon_key = f"icon_{opt['key']}"
            else:
                icon_key = f"icon_{opt['key']}"
                
            icon_surf = self.assets.get_surface(icon_key, (64, 64), icon_key)
            icon_rect = icon_surf.get_rect(midleft=(rect_bg.left + 20, rect_bg.centery))
            self.display_surface.blit(icon_surf, icon_rect)
            
            text_x = rect_bg.left + 100
            
            title = f"{i+1}. {opt['display_name']}"
            if opt['lvl'] == 0: title
            else: title += f" (Lvl {opt['lvl']} -> {opt['lvl']+1})"
            
            title_surf = self.font.render(title, True, (255, 255, 0))
            self.display_surface.blit(title_surf, (text_x, rect_bg.top + 15))
            
            desc_surf = self.assets.load_font(24).render(opt['desc'], True, (200, 200, 200))
            self.display_surface.blit(desc_surf, (text_x, rect_bg.top + 55))
            
            start_y += 120
            
class GameOverMenu(Menu):
    def __init__(self, font):
        super().__init__(font)
        self.options = ['TENTAR NOVAMENTE', 'MENU PRINCIPAL', 'SAIR']
        self.selected_index = 0
        self.stats = {}
        self.assets = AssetManager()

    def set_stats(self, player, game_time_ms):
        seconds = int(game_time_ms / 1000) % 60
        minutes = int(game_time_ms / 1000 / 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        self.stats = {
            'level': player.level,
            'time': time_str,
            'kills': player.kill_count,
            'gold': int(player.credits)
        }

    def draw(self):
        # Fundo escuro avermelhado (Sangue/Derrota)
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 200))
        self.display_surface.blit(overlay, (0,0))
        
        # Título
        self.draw_text("REPROVADO!", 80, WIDTH//2, 100, (255, 50, 50))
        self.draw_text("Resumo do Semestre", 30, WIDTH//2, 160, (200, 200, 200))

        # --- PAINEL DE ESTATÍSTICAS ---
        panel_rect = pygame.Rect(0, 0, 500, 250)
        panel_rect.center = (WIDTH//2, HEIGHT//2 - 20)
        pygame.draw.rect(self.display_surface, (20, 20, 30), panel_rect)
        pygame.draw.rect(self.display_surface, (255, 50, 50), panel_rect, 2)
        
        # Linhas de Stats
        stats_list = [
            ("Tempo de Prova:", self.stats.get('time', "00:00")),
            ("Período Alcançado:", str(self.stats.get('level', 1))),
            ("Questões Resolvidas (Abates):", str(self.stats.get('kills', 0))),
            ("Créditos Obtidos:", str(self.stats.get('gold', 0)))
        ]
        
        start_y = panel_rect.top + 40
        for label, value in stats_list:
            # Label à esquerda
            label_surf = self.assets.load_font(28).render(label, True, (200, 200, 200))
            label_rect = label_surf.get_rect(midleft=(panel_rect.left + 40, start_y))
            self.display_surface.blit(label_surf, label_rect)
            
            # Valor à direita
            val_surf = self.assets.load_font(32).render(value, True, (255, 215, 0))
            val_rect = val_surf.get_rect(midright=(panel_rect.right - 40, start_y))
            self.display_surface.blit(val_surf, val_rect)
            
            start_y += 50

        # --- OPÇÕES ---
        opt_y_start = HEIGHT - 180
        for index, option in enumerate(self.options):
            color = COLORS['selected_option'] if index == self.selected_index else COLORS['unselected_option']
            y_pos = opt_y_start + index * 50
            
            text = f"> {option} <" if index == self.selected_index else option
            self.draw_text(text, 35, WIDTH//2, y_pos, color)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                if event.key in [pygame.K_DOWN, pygame.K_s]:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE]:
                    if self.selected_index == 0: return 'restart'
                    elif self.selected_index == 1: return 'main_menu'
                    elif self.selected_index == 2: return 'quit'
        return None