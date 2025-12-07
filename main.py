import pygame, sys
from settings import *
from player import Player
from enemy import Enemy
from random import choice, randint

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        self.bg_surf = pygame.image.load('assets/background.png').convert()
        self.bg_rect = self.bg_surf.get_rect(topleft=(0,0))
        
        # FIX: Pega o tamanho REAL da imagem em vez de confiar no settings
        self.bg_w = self.bg_surf.get_width()
        self.bg_h = self.bg_surf.get_height()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        # --- FIX DO BACKGROUND (Agora calcula matematicamente) ---
        bg_w = self.bg_surf.get_width()
        bg_h = self.bg_surf.get_height()

        # Calcula a posição inicial do grid (arredondando para o tile mais próximo)
        start_col = int(self.offset.x // bg_w)
        start_row = int(self.offset.y // bg_h)
        
        # Calcula QUANTOS tiles cabem na tela (+ 2 de margem pra garantir)
        # O int() + 1 arredonda pra cima pra não faltar pedaço
        num_cols = (WIDTH // bg_w) + 2
        num_rows = (HEIGHT // bg_h) + 2
        
        # Desenha apenas os tiles visíveis
        for col in range(start_col - 1, start_col + num_cols):
            for row in range(start_row - 1, start_row + num_rows):
                x = col * bg_w
                y = row * bg_h
                pos = (x - self.offset.x, y - self.offset.y)
                self.display_surface.blit(self.bg_surf, pos)

        # --- FIM DO FIX ---

        # Desenha os Sprites (essa parte continua igual)
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
            # (Mantém o código da UI/Barras aqui...)
            if hasattr(sprite, 'draw_ui'):
                 # ... código das barras de vida/xp ...
                 # (Se quiser, posso reenviar esse trecho, mas é só manter o que já tinha)
                 ui_x = offset_pos[0] + sprite.image.get_width() // 2 - 30
                 ui_y = offset_pos[1] + sprite.image.get_height() + 10
                 
                 pygame.draw.rect(self.display_surface, BLACK, (ui_x, ui_y, 60, 10))
                 ratio = max(0, sprite.health) / sprite.max_health
                 pygame.draw.rect(self.display_surface, RED, (ui_x, ui_y, 60 * ratio, 10))
                 
                 xp_ratio = sprite.xp / sprite.next_level_xp
                 pygame.draw.rect(self.display_surface, BLACK, (ui_x, ui_y + 12, 60, 5))
                 pygame.draw.rect(self.display_surface, BLUE, (ui_x, ui_y + 12, 60 * xp_ratio, 5))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.running = True

    def create_sprites(self):
        # Usa o grupo de câmera agora
        self.all_sprites = CameraGroup()
        self.enemies = pygame.sprite.Group() 
        self.xp_group = pygame.sprite.Group()

        # O player nasce no 0,0 do mundo (mas a câmera vai centralizar ele)
        self.player = Player((0, 0), [self.all_sprites], self.enemies, self.xp_group)
        
        # Timer de spawn
        self.spawn_timer = pygame.time.get_ticks()

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > ENEMY_SPAWN_TIME:
            self.spawn_timer = current_time
            
            # Spawna inimigo num raio fora da tela (entre 700 e 900 de distancia)
            dist = randint(700, 900)
            angle = randint(0, 360)
            
            # Matemática pra achar o x,y baseado no angulo
            import math
            spawn_x = self.player.rect.centerx + dist * math.cos(math.radians(angle))
            spawn_y = self.player.rect.centery + dist * math.sin(math.radians(angle))
            
            Enemy((spawn_x, spawn_y), [self.all_sprites, self.enemies], self.player, self.xp_group)

    def check_collisions(self):
        # Dano do Inimigo no Player
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.player.take_damage(10)
            
        # Projetil acertando inimigo
        # Como projetil tá no all_sprites, a gente precisa filtrar
        projectiles = [s for s in self.all_sprites if hasattr(s, 'damage')]
        
        for p in projectiles:
            hit_enemies = pygame.sprite.spritecollide(p, self.enemies, False)
            if hit_enemies:
                for e in hit_enemies:
                    e.take_damage(p.damage)
                p.kill() # Bala some ao bater

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(midtop=(x, y))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.spawn_enemy()
        self.check_collisions()
        
        if not self.player.alive():
            self.playing = False 

    def draw(self):
        self.screen.fill(BLACK)
        
        # Chama o draw customizado da câmera passando o player como foco
        self.all_sprites.custom_draw(self.player)
        
        # UI Fixa na tela (Score, Level)
        self.draw_text(f"Level: {self.player.level}", 30, WHITE, 60, 20)
        
        pygame.display.flip()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(TITLE, 60, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Sobreviva à UFRPE!", 30, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("WASD move | O personagem atira sozinho", 25, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        self.draw_text("[ENTER] para começar", 30, RED, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if not self.running: return
        self.screen.fill(BLACK)
        self.draw_text("REPROVADO PELO CLEYTON", 60, RED, WIDTH / 2, HEIGHT / 4)
        self.draw_text(f"Nível alcançado: {self.player.level}", 40, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("[R] Tentar de novo | [ESC] Menu", 30, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r: waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.show_start_screen()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN: waiting = False

if __name__ == '__main__':
    game = Game()
    game.show_start_screen()
    while game.running:
        game.create_sprites()
        game.run()
        game.show_go_screen()
    pygame.quit()
    sys.exit()