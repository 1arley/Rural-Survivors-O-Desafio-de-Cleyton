import pygame

# --- CONFIGURAÇÕES DO APLICATIVO ---
class AppConfig:
    TITLE = "UFRPE Survivors: A Jornada Acadêmica"
    WIDTH = 1280
    HEIGHT = 720
    FPS = 60
    TILE_SIZE = 64

# --- PALETA DE CORES (Definições Puras) ---
class Colors:
    WHITE       = (255, 255, 255)
    BLACK       = (0, 0, 0)
    RED         = (255, 0, 0)
    GREEN       = (0, 255, 0)
    BLUE        = (0, 0, 255)
    YELLOW      = (255, 255, 0)
    CYAN        = (0, 255, 255)
    MAGENTA     = (255, 0, 255)
    ORANGE      = (255, 165, 0)
    PURPLE      = (128, 0, 128)
    GRAY        = (100, 100, 100)
    DARK_GRAY   = (50, 50, 50)
    GOLD        = (255, 215, 0)
    DARK_BLUE   = (30, 30, 40)
    BROWN       = (139, 69, 19)
    RED_ORANGE  = (255, 69, 0)
    DARK_RED    = (139, 0, 0)
    LIME        = (50, 205, 50)
    NAVY        = (0, 0, 128)
    PINK        = (255, 105, 180)

# --- MAPA DE CORES DO JOGO (Semântico) ---
ENTITY_COLORS = {
    # UI
    'menu_bg': Colors.DARK_BLUE, 
    'title_text': Colors.GOLD,
    'selected_option': Colors.WHITE,
    'unselected_option': Colors.GRAY,
    'bg': (20, 20, 25), 
    'grid': (40, 40, 50),
    'text': Colors.WHITE,
    'ui_bg': (0, 0, 0, 150),        
    
    # Entidades (Player)
    'player_calouro': Colors.GREEN,       
    'player_veterano': Colors.BLUE,
    'player_monitor': Colors.PURPLE,
    'player_pesquisador': Colors.GOLD,    
    
    # Inimigos
    'enemy_basic': (200, 50, 50),    
    'enemy_fast': Colors.ORANGE,
    'enemy_tank': Colors.PURPLE,
    'enemy_ranged': Colors.LIME,
    'enemy_elite': Colors.NAVY,
    'enemy_boss': Colors.GOLD,
    
    # Drops
    'xp_small': Colors.CYAN,         
    'xp_medium': Colors.GREEN,          
    'xp_large': Colors.GOLD,           
    'chest': (150, 100, 50),
    'pickup_heart': Colors.RED, 
    'pickup_chest': Colors.GOLD,
    'elite_crown': Colors.GOLD,
    
    # Armas & Efeitos
    'proj': Colors.YELLOW,
    'proj_caderno': Colors.WHITE,     
    'proj_caneta': Colors.BLUE,          
    'area_giz': (255, 255, 255, 100),
    'whip_sprite': (200, 50, 50),
    'proj_cafe_chao': Colors.BROWN,
    'proj_area_fogo': Colors.RED_ORANGE,
    'proj_estilete': Colors.GRAY,
    'proj_enemy': Colors.MAGENTA,
    'proj_protocolo': Colors.CYAN,

    # Ícones (Fallbacks)
    'icon_default': Colors.WHITE,
    
    # Ícones de Armas
    'icon_caderno': Colors.WHITE, 'icon_regua': Colors.GRAY,
    'icon_cafe_chao': Colors.BROWN, 'icon_curto_circuito': Colors.YELLOW,
    'icon_molotov_quimica': Colors.ORANGE, 'icon_eletrons': Colors.CYAN,
    'icon_lapis_b': Colors.DARK_GRAY, 'icon_cabo_rede': Colors.BLUE,
    'icon_roteador': Colors.LIME, 'icon_livro_calculo': Colors.RED,
    'icon_projetor': Colors.WHITE, 'icon_ventilador': Colors.CYAN,
    'icon_estilete': Colors.GRAY, 'icon_protocolo': Colors.WHITE,
    
    # Ícones de Passivos
    'icon_tenis': Colors.WHITE, 'icon_energetico': Colors.CYAN,
    'icon_oculos': Colors.RED, 'icon_matricula': Colors.GRAY,
    'icon_bolsa': Colors.GOLD, 'icon_marmita': Colors.GREEN,
    'icon_argumento': Colors.PURPLE, 'icon_caneta_vermelha': Colors.RED,
    'icon_internet': Colors.BLUE, 'icon_rede': (255, 100, 200),
    'icon_cracha': (100, 100, 150), 'icon_megafone': Colors.YELLOW,
    'icon_ima': (50, 50, 255), 'icon_cafe_forte': Colors.BROWN,
    'icon_xerox': (200, 200, 200), 'icon_mochila': (0, 50, 100)
}

# --- CONFIGURAÇÃO DE CAMADAS ---
class Layers:
    GROUND = 0
    ITEMS = 1
    MAIN = 2
    FLYING = 3
    UI = 4

# --- CAMINHOS DOS ARQUIVOS ---
ASSET_PATHS = {
    'title_screen': 'assets/ui/title_screen.png',
    'ui_frame': 'assets/ui/frame_border.png',
    'ui_xp_bar_empty': 'assets/ui/xp_bar_empty.png',
    'ui_xp_bar_full': 'assets/ui/xp_bar_full.png',
    'ui_pause_bg': 'assets/ui/pause_bg.png',
    'bg_campus': 'assets/environment/campus_floor.png', 

    'player': 'assets/player.png',
    'player_calouro': 'assets/player.png', 
    'player_veterano': 'assets/player_veterano.png',
    'player_monitor': 'assets/monitor.png',
    'player_pesquisador': 'assets/player_pesquisador.png',
    
    'lista_exercicio': 'assets/enemies/basic.png',
    'seminario': 'assets/enemies/elite.png',
    'gato_campus': 'assets/enemies/fast.png',
    'onibus_lotado': 'assets/enemies/tank.png',
    'ead': 'assets/enemies/ranged.png',
    'banca': 'assets/enemies/mini_boss.png',
    'coordenador': 'assets/enemies/mid_boss.png',
    'reitoria': 'assets/enemies/final_boss.png',
    'xp_gem': 'assets/items/xp_gem.png',
    'chest': 'assets/items/chest.png',
    'pickup_heart': 'assets/items/heart.png',
    
    'proj': 'assets/weapons/projectile_generic.png',
    'proj_enemy': 'assets/enemies/projectile.png',
    'proj_caderno': 'assets/weapons/caderno_proj.png',
    'proj_caneta': 'assets/weapons/caneta_proj.png',
    'area_giz': 'assets/weapons/aura_generic.png',
    'whip_sprite': 'assets/weapons/cabo_rede_whip.png',
    'proj_cafe_chao': 'assets/weapons/cafe_chao.png',
    'proj_protocolo': 'assets/weapons/protocolo_proj.png',
    'proj_area_fogo': 'assets/weapons/molotov_area.png',

    'icon_caderno': 'assets/icons/weapons/caderno.png',
    'icon_regua': 'assets/icons/weapons/regua.png',
    'icon_protocolo': 'assets/icons/weapons/protocolo.png',
    'icon_cafe_chao': 'assets/icons/weapons/cafe_chao.png',
    'icon_curto_circuito': 'assets/icons/weapons/curto_circuito.png',
    'icon_molotov_quimica': 'assets/icons/weapons/molotov.png',
    'icon_eletrons': 'assets/icons/weapons/eletrons.png',
    'icon_lapis_b': 'assets/icons/weapons/lapis.png',
    'icon_cabo_rede': 'assets/icons/weapons/cabo_rede.png',
    'icon_roteador': 'assets/icons/weapons/roteador.png',
    'icon_livro_calculo': 'assets/icons/weapons/livro_calculo.png',
    'icon_projetor': 'assets/icons/weapons/projetor.png',
    'icon_ventilador': 'assets/icons/weapons/ventilador.png',
    
    'icon_tenis': 'assets/icons/upgrades/agility.png',
    'icon_energetico': 'assets/icons/upgrades/cooldown.png',
    'icon_oculos': 'assets/icons/upgrades/damage.png',
    'icon_matricula': 'assets/icons/upgrades/evasion.png',
    'icon_bolsa': 'assets/icons/upgrades/gold.png',
    'icon_marmita': 'assets/icons/upgrades/health.png',
    'icon_argumento': 'assets/icons/upgrades/knockback.png',
    'icon_caneta_vermelha': 'assets/icons/upgrades/precision.png',
    'icon_internet': 'assets/icons/upgrades/projectile_speed.png',
    'icon_rede': 'assets/icons/upgrades/regen.png',
    'icon_cracha': 'assets/icons/upgrades/armor.png',
    'icon_megafone': 'assets/icons/upgrades/area.png',
    'icon_ima': 'assets/icons/upgrades/magnet.png',
    'icon_cafe_forte': 'assets/icons/upgrades/duration.png',
    'icon_xerox': 'assets/icons/upgrades/quantity.png',
    'icon_mochila': 'assets/icons/upgrades/xp.png',
}

# --- Compatibilidade com código antigo ---
WIDTH = AppConfig.WIDTH
HEIGHT = AppConfig.HEIGHT
FPS = AppConfig.FPS
TILE_SIZE = AppConfig.TILE_SIZE
TITLE = AppConfig.TITLE
COLORS = ENTITY_COLORS