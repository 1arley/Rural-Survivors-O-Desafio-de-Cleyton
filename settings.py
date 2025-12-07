import pygame

# --- Configurações Gerais ---
TITLE = "UFRPE Survivors: A Jornada Acadêmica"
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILE_SIZE = 64

# --- Cores (Placeholders) ---
# Temática UFRPE: Verdes, Vermelhos (Prazos), Dourado (Aprovação)
COLORS = {
    'bg': (20, 20, 25),             # Fundo escuro
    'grid': (40, 40, 50),           # Grid do chão
    'text': (255, 255, 255),
    'ui_bg': (0, 0, 0, 150),        # Transparente
    
    # Entidades
    'player_calouro': (0, 200, 0),       # Verde UFRPE
    'player_veterano': (0, 100, 255),    # Azul
    'enemy_basic': (200, 50, 50),        # Vermelho (Prazo)
    'enemy_fast': (255, 150, 0),         # Laranja (Grupo)
    'enemy_tank': (100, 0, 100),         # Roxo (Prova Final)
    'enemy_boss': (255, 0, 0),           # Vermelho Sangue (TCC)
    
    # Drops
    'xp_small': (100, 255, 255),         # Ciano (Artigo)
    'xp_medium': (0, 255, 100),          # Verde (Livro)
    'xp_large': (255, 215, 0),           # Ouro (Diploma)
    'chest': (150, 100, 50),             # Marrom (Baú/Mesa)
    
    # Armas
    'proj_caderno': (255, 255, 255),     # Branco
    'proj_caneta': (0, 0, 255),          # Azul Bic
    'area_giz': (255, 255, 255, 100)     # Branco Transparente
}

# --- Grupos de Camadas (Renderização) ---
LAYERS = {
    'ground': 0,
    'items': 1,
    'main': 2,
    'flying': 3,
    'ui': 4
}

ASSET_PATHS = {
    # Player
    'player': 'assets/player.png',
    
    # Inimigos (As chaves devem ser iguais aos nomes no JSON/Enemy class)
    'prazo_curto': 'assets/enemies/prazo_curto.png',
    'trabalho_grupo': 'assets/enemies/trabalho_grupo.png',
    'prova_final': 'assets/enemies/prova_final.png',
    'tcc': 'assets/enemies/tcc.png',
    
    # Itens/Armas
    'xp_gem': 'assets/items/xp_gem.png',
    'proj': 'assets/items/projectile.png'
}