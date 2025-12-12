import pygame
import sys
import random
from settings import *
from src.utils.helpers import AssetManager, import_json
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.weapons.controller import WeaponController
from src.ui.hud import UI
from src.ui.menu import CharacterSelectMenu, LevelUpMenu, MainMenu, PauseMenu, ShopMenu, GameOverMenu
from src.ui.damage_text import DamageText 
from src.systems.camera import CameraGroup
from src.items.xp_orb import ExperienceGem
from src.items.pickup import Pickup 
from src.systems.progression import UpgradeManager
from src.systems.save_manager import SaveManager
from src.systems.wave_manager import WaveManager
from src.ui.particles import Particle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 40)
        
        self.balance_data = import_json('data/balance.json')
        self.upgrade_manager = UpgradeManager(self.balance_data)
        self.save_manager = SaveManager()
        self.wave_manager = WaveManager(self)

        self.main_menu = MainMenu(self.font) 
        self.char_select_menu = CharacterSelectMenu(self.font, self.balance_data['characters'])
        self.level_up_menu = LevelUpMenu(self.font)
        self.pause_menu = PauseMenu(self.font, self)
        self.shop_menu = ShopMenu(self.font)
        self.game_over_menu = GameOverMenu(self.font)

        self.state = 'main_menu'
        self.current_upgrade_options = []
        self.game_time = 0

    def start_game(self, char_key):
        self.all_sprites = CameraGroup() 
        self.enemy_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.xp_sprites = pygame.sprite.Group()
        self.damage_text_sprites = pygame.sprite.Group() 
        self.enemy_projectile_sprites = pygame.sprite.Group()
        self.pickup_sprites = pygame.sprite.Group()
        
        player_groups = [self.all_sprites, self.damage_text_sprites]

        self.groups = {
            'all_sprites': self.all_sprites,
            'enemy_sprites': self.enemy_sprites,
            'attack_sprites': self.attack_sprites,
            'xp_sprites': self.xp_sprites,
            'damage_text': self.damage_text_sprites,
            'enemy_projectiles': self.enemy_projectile_sprites,
            'pickups': self.pickup_sprites
        }
        
        char_data = self.balance_data['characters'][char_key]
        
        self.player = Player(
            pos=(WIDTH//2, HEIGHT//2), 
            groups=player_groups,  
            obstacles_sprites=None, 
            create_attack=None, 
            destroy_attack=None,
            char_data=char_data
        )
        
        self.weapon_controller = WeaponController(self.player, self.groups, self.balance_data)
        self.player.weapon_controller = self.weapon_controller 
        
        if char_key == 'calouro': self.weapon_controller.add_weapon('caderno')
        elif char_key == 'veterano': self.weapon_controller.add_weapon('cabo_rede')
        elif char_key == 'monitor': self.weapon_controller.add_weapon('protocolo')
        elif char_key == 'pesquisador': self.weapon_controller.add_weapon('eletrons')
            
        self.ui = UI()
        self.game_time = 0 # Tempo começa do zero
        self.wave_manager = WaveManager(self)
        self.state = 'playing'

    def spawn_enemy(self, enemy_type=None):
        # Garante que o player existe para pegar a posição dele
        if not hasattr(self, 'player') or not self.player:
            return

        side = random.choice(['top', 'bottom', 'left', 'right'])
        offset = 50 
        
        # Pega a posição central do jogador no mundo
        px, py = self.player.rect.center
        
        # Calcula as bordas da visão (Câmera) baseadas no Player
        # (WIDTH e HEIGHT vêm do settings.py)
        camera_left = px - (WIDTH // 2)
        camera_right = px + (WIDTH // 2)
        camera_top = py - (HEIGHT // 2)
        camera_bottom = py + (HEIGHT // 2)

        # Gera coordenadas RELATIVAS à câmera atual
        if side == 'top':
            x = random.randint(int(camera_left), int(camera_right))
            y = int(camera_top - offset)
            pos = (x, y)
        elif side == 'bottom':
            x = random.randint(int(camera_left), int(camera_right))
            y = int(camera_bottom + offset)
            pos = (x, y)
        elif side == 'left':
            x = int(camera_left - offset)
            y = random.randint(int(camera_top), int(camera_bottom))
            pos = (x, y)
        else: # right
            x = int(camera_right + offset)
            y = random.randint(int(camera_top), int(camera_bottom))
            pos = (x, y)
        
        if not enemy_type: enemy_type = 'lista_exercicio'
        
        if enemy_type in self.balance_data['enemies']:
            stats = self.balance_data['enemies'][enemy_type]
            is_elite = False
            if not stats.get('is_boss', False) and random.random() < 0.05:
                is_elite = True
            
            e = Enemy(enemy_type, pos, [self.all_sprites, self.enemy_sprites], self.player, stats, is_elite)
            e.projectile_groups = [self.all_sprites, self.enemy_projectile_sprites]
        else:
            print(f"AVISO: Inimigo '{enemy_type}' não encontrado")

    def check_collisions(self):
        # 1. ATAQUES DO PLAYER vs INIMIGOS
        attack_hits = pygame.sprite.groupcollide(self.enemy_sprites, self.attack_sprites, False, False)
        
        for enemy, attacks in attack_hits.items():
            for attack in attacks:
                if hasattr(attack, 'data'):
                    if 'slow' in attack.data: enemy.apply_slow(attack.data['slow'], 200)
                    if 'burn_damage' in attack.data: enemy.apply_burn(attack.data['burn_damage'], attack.data.get('burn_duration', 2000))

                base_damage = attack.damage
                is_crit = False
                weapon_crit_bonus = attack.data.get('crit_chance_bonus', 0) if hasattr(attack, 'data') else 0
                if random.randint(0, 100) < (self.player.modifiers['crit_chance'] + weapon_crit_bonus):
                    is_crit = True
                    base_damage *= self.player.modifiers['crit_mult']
                final_damage = int(base_damage)
                
                took_damage = False
                is_persistent = hasattr(attack, 'is_persistent') and attack.is_persistent
                
                if attack.type != 'projectile' or is_persistent:
                    if enemy not in attack.hit_list:
                        enemy.health -= final_damage
                        attack.hit_list.append(enemy)
                        took_damage = True
                else:
                    if enemy not in attack.ignored_enemies:
                        enemy.health -= final_damage
                        attack.ignored_enemies.append(enemy)
                        took_damage = True
                        if hasattr(attack, 'bounces_left') and attack.bounces_left > 0: attack.bounces_left -= 1
                        elif hasattr(attack, 'pierce_left') and attack.pierce_left > 0: attack.pierce_left -= 1
                        else: attack.kill() 

                if took_damage:
                    enemy.trigger_flash()
                    offset_x = random.randint(-20, 20)
                    offset_y = random.randint(-20, 20)
                    DamageText((enemy.rect.centerx+offset_x, enemy.rect.centery+offset_y), final_damage, [self.all_sprites, self.damage_text_sprites], is_crit)
                    
                    base_kb = attack.data.get('knockback', 0) if hasattr(attack, 'data') else 0
                    total_kb = base_kb + self.player.modifiers['knockback']
                    if total_kb > 0:
                        direction = (pygame.math.Vector2(enemy.rect.center) - self.player.rect.center).normalize()
                        enemy.apply_knockback(direction, total_kb)

            if enemy.health <= 0:
                ExperienceGem(enemy.rect.center, enemy.xp_value, [self.all_sprites, self.xp_sprites], self.player)
                
                if enemy.is_boss:
                    Pickup(enemy.rect.center, 'chest', [self.all_sprites, self.pickup_sprites])
                elif enemy.is_elite:
                    roll = random.random()
                    if roll < 0.10: Pickup(enemy.rect.center, 'chest', [self.all_sprites, self.pickup_sprites])
                    elif roll < 0.40: Pickup(enemy.rect.center, 'heart', [self.all_sprites, self.pickup_sprites])
                else:
                    # Chance mínima (0.05%) para comuns
                    if random.random() < 0.0005:
                        Pickup(enemy.rect.center, 'heart', [self.all_sprites, self.pickup_sprites])

                p_color = COLORS.get(enemy.color_key, (200, 50, 50))
                for _ in range(5):
                    Particle(enemy.rect.center, p_color, [self.all_sprites])
                enemy.kill()
                self.player.credits += 1 * self.player.modifiers.get('gold_gain', 1.0)
                self.player.kill_count += 1

        # 2. INIMIGOS (CORPO) vs PLAYER
        player_hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
        if player_hits: 
            damage = player_hits[0].damage 
            self.player.take_damage(damage)
            if not self.player.invulnerable: self.all_sprites.shake(10, 20) 
        
        # 3. TIROS INIMIGOS vs PLAYER
        projectile_hits = pygame.sprite.spritecollide(self.player, self.enemy_projectile_sprites, True)
        if projectile_hits:
            damage = projectile_hits[0].damage
            self.player.take_damage(damage)
            if not self.player.invulnerable: self.all_sprites.shake(8, 15)

        # 4. PICKUPS
        pickup_hits = pygame.sprite.spritecollide(self.player, self.pickup_sprites, True)
        for pickup in pickup_hits:
            if pickup.type == 'heart':
                self.player.health = min(self.player.stats['hp'], self.player.health + pickup.value)
                DamageText(self.player.rect.midtop, f"+{pickup.value}", [self.all_sprites, self.damage_text_sprites], False)
            elif pickup.type == 'chest':
                self.generate_upgrade_options()
                self.state = 'level_up'

        if self.player.health <= 0:
            self.state = 'game_over'
            self.save_manager.add_credits(self.player.credits)
            self.game_over_menu.set_stats(self.player, self.game_time)

    def generate_upgrade_options(self):
        self.current_upgrade_options = self.upgrade_manager.get_random_options(
            self.player, self.weapon_controller, count=3
        )
        self.level_up_menu.set_options(self.current_upgrade_options)

    def apply_upgrade(self, index):
        if index < len(self.current_upgrade_options):
            choice = self.current_upgrade_options[index]
            if choice['type'] == 'weapon':
                self.weapon_controller.add_weapon(choice['key'])
            elif choice['type'] == 'passive':
                self.player.apply_passive(choice['key'], choice['data'])
            self.state = 'playing'

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            if self.state == 'main_menu':
                action = self.main_menu.handle_input()
                if action == 'quit': self.running = False
                elif action == 'play': self.state = 'character_select'
                elif action == 'shop': self.state = 'shop'
                self.main_menu.draw()
                pygame.display.flip()
                continue

            if self.state == 'shop':
                action = self.shop_menu.handle_input()
                if action == 'back': self.state = 'main_menu'
                elif action == 'quit': self.running = False
                self.shop_menu.draw()
                pygame.display.flip()
                continue

            if self.state == 'character_select':
                result = self.char_select_menu.handle_input()
                if result == 'quit': 
                    self.running = False  # Fecha o jogo se clicar no X
                elif result == 'back': 
                    self.state = 'main_menu'  # Volta pro menu se apertar ESC
                elif result: 
                    self.start_game(result)  # Inicia o jogo apenas se for um personagem válido
                self.char_select_menu.draw()
                pygame.display.flip()
                continue

            if self.state == 'playing':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: self.running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.state = 'paused'
                
                # --- CORREÇÃO: CALCULAMOS O TEMPO INTERNAMENTE ---
                self.game_time += dt * 1000 
                
                # Atualiza Wave Manager com o tempo corrigido
                self.wave_manager.update(self.game_time)

                self.all_sprites.update(dt)
                self.weapon_controller.update()
                self.check_collisions() 
                
                if self.player.xp >= self.player.next_level_xp:
                    self.player.level_up()
                    self.generate_upgrade_options()
                    self.state = 'level_up'

                self.screen.fill(COLORS['bg'])
                self.all_sprites.custom_draw(self.player)
                self.ui.display(self.player, self.game_time)

            if self.state == 'paused':
                self.screen.fill(COLORS['bg'])
                self.all_sprites.custom_draw(self.player)
                self.ui.display(self.player, self.game_time)
                action = self.pause_menu.handle_input()
                if action == 'resume': 
                    self.state = 'playing'
                elif action == 'main_menu': 
                    self.save_manager.add_credits(self.player.credits)
                    self.state = 'main_menu'
                elif action == 'quit_game': 
                    self.save_manager.add_credits(self.player.credits)
                    self.running = False
                self.pause_menu.draw()

            if self.state == 'level_up':
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: self.running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1: self.apply_upgrade(0)
                        elif event.key == pygame.K_2: self.apply_upgrade(1)
                        elif event.key == pygame.K_3: self.apply_upgrade(2)
                self.all_sprites.custom_draw(self.player) 
                self.level_up_menu.draw()
            
            elif self.state == 'game_over':
                action = self.game_over_menu.handle_input()
                if action == 'quit': self.running = False
                elif action == 'main_menu': self.state = 'main_menu'
                elif action == 'restart': self.state = 'character_select'
                
                self.all_sprites.custom_draw(self.player)
                self.game_over_menu.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    Game().run()