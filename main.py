import pygame
import sys
import random
from settings import *
from src.utils.helpers import AssetManager, import_json
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.weapons.weapon import WeaponController
from src.ui.hud import UI
from src.systems.camera import CameraGroup
from src.items.xp_orb import ExperienceGem
from src.systems.progression import EvolutionSystem

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 40)
        
        self.balance_data = import_json('data/balance.json')

        self.all_sprites = CameraGroup() 
        self.enemy_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.xp_sprites = pygame.sprite.Group()
        
        self.groups = {
            'all_sprites': self.all_sprites,
            'enemy_sprites': self.enemy_sprites,
            'attack_sprites': self.attack_sprites,
            'xp_sprites': self.xp_sprites
        }
        
        self.player = Player((WIDTH//2, HEIGHT//2), [self.all_sprites], None, None, None)
        
        # Simulando passivos para testar evolução (em um jogo real, você pegaria no level up)
        self.player.passives = [{'name': 'Calculadora', 'level': 6}] 
        
        self.weapon_controller = WeaponController(self.player, self.groups)
        self.weapon_controller.add_weapon('caderno')
        # Hack para testar evolução rápido:
        self.weapon_controller.weapons_data['caderno']['lvl'] = 8 
        
        self.ui = UI()
        self.evolution_system = EvolutionSystem() # Instancia o sistema
        
        self.start_time = pygame.time.get_ticks()
        self.enemy_timer = 0
        self.enemy_spawn_rate = 1000
        self.state = 'playing' # 'playing', 'level_up', 'game_over'

    def spawn_enemy(self):
        # Spawna nas bordas da tela
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top': pos = (random.randint(0, WIDTH), -50)
        elif side == 'bottom': pos = (random.randint(0, WIDTH), HEIGHT + 50)
        elif side == 'left': pos = (-50, random.randint(0, HEIGHT))
        else: pos = (WIDTH + 50, random.randint(0, HEIGHT))
        
        # Define tipo baseado no tempo
        minutes = (pygame.time.get_ticks() - self.start_time) / 60000
        enemy_type = 'prazo_curto'
        if minutes > 1: enemy_type = 'trabalho_grupo'
        if minutes > 3: enemy_type = 'prova_final'
        
        stats = self.balance_data['enemies'][enemy_type]
        Enemy(enemy_type, pos, [self.all_sprites, self.enemy_sprites], self.player, stats)

    def check_collisions(self):
        # Ataques vs Inimigos
        hits = pygame.sprite.groupcollide(self.enemy_sprites, self.attack_sprites, False, False)
        for enemy, attacks in hits.items():
            for attack in attacks:
                enemy.health -= attack.damage
            
            if enemy.health <= 0:
                # CORREÇÃO AQUI: Passar self.player como argumento
                ExperienceGem(enemy.rect.center, enemy.xp_value, [self.all_sprites, self.xp_sprites], self.player)
                enemy.kill()

        # Inimigos vs Player
        hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
        for enemy in hits:
            self.player.health -= 0.5
            if self.player.health <= 0:
                self.state = 'game_over'
                
        # Inimigos vs Player
        hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
        for enemy in hits:
            self.player.health -= 0.5 # Dano de contato contínuo
            if self.player.health <= 0:
                self.state = 'game_over'

    def draw_level_up_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0,0))
        
        text = self.font.render("CONHECIMENTO ADQUIRIDO! (Escolha: 1, 2 ou 3)", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH//2, 100))
        self.screen.blit(text, rect)
        
        # Placeholder para opções (usaria botões reais aqui)
        options = [
            "1. Melhorar Caderno",
            "2. Adicionar Caneta",
            "3. Café Forte (+Speed)"
        ]
        for i, opt in enumerate(options):
            opt_surf = self.font.render(opt, True, (255, 255, 0))
            self.screen.blit(opt_surf, (WIDTH//2 - 100, 250 + i*60))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            current_time = pygame.time.get_ticks() - self.start_time
            
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == 'level_up':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.weapon_controller.weapons_data['caderno']['damage'] += 5
                            self.state = 'playing'
                        elif event.key == pygame.K_2:
                            self.weapon_controller.add_weapon('caneta')
                            self.state = 'playing'
                        elif event.key == pygame.K_3:
                            self.player.stats['speed'] += 20
                            self.state = 'playing'

            # Logic
            if self.state == 'playing':
                # Spawn Enemies
                if pygame.time.get_ticks() - self.enemy_timer > self.enemy_spawn_rate:
                    self.spawn_enemy()
                    self.enemy_timer = pygame.time.get_ticks()
                    # Acelera o spawn com o tempo
                    self.enemy_spawn_rate = max(200, 1000 - (current_time / 1000))

                self.all_sprites.update(dt)
                self.weapon_controller.update()
                self.check_collisions()
                
                # Check Level Up (simplificado para exemplo)
                if self.player.xp >= self.player.next_level_xp:
                    self.player.level_up()
                    self.state = 'level_up'

            # Drawing
            self.screen.fill(COLORS['bg'])
            
            # Draw Grid (efeito visual)
            for x in range(0, WIDTH, TILE_SIZE):
                pygame.draw.line(self.screen, COLORS['grid'], (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, TILE_SIZE):
                pygame.draw.line(self.screen, COLORS['grid'], (0, y), (WIDTH, y))

            # Draw All Sprites (na ordem correta seria via Câmera/Layer)
            self.all_sprites.custom_draw(self.player)
            
            # UI
            self.ui.display(self.player, pygame.time.get_ticks() - self.start_time)
            
            if self.state == 'level_up':
                self.draw_level_up_screen()
            elif self.state == 'game_over':
                go_surf = self.font.render("REPROVADO POR FALTA!", True, (255, 0, 0))
                go_rect = go_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
                self.screen.blit(go_surf, go_rect)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Game().run()