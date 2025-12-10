import pygame
import json
import os
# Importa as novas classes e o dicionário de cores
from settings import ENTITY_COLORS, ASSET_PATHS 

class AssetManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.assets = {}
            cls._instance.fonts = {}
        return cls._instance

    def load_font(self, size):
        key = f"font_{size}"
        if key not in self.fonts:
            # Tenta carregar fonte padrão do sistema se não tiver arquivo
            self.fonts[key] = pygame.font.Font(None, size)
        return self.fonts[key]

    def get_surface(self, key, target_size=None, color_key='player_calouro', scale_factor=None, shape='rect'):
        if isinstance(scale_factor, str):
            shape = scale_factor
            scale_factor = None

        cache_key = (key, target_size, scale_factor, shape)
        
        if cache_key in self.assets:
            return self.assets[cache_key]
        
        image = None

        if key in ASSET_PATHS:
            path = ASSET_PATHS[key]
            if os.path.exists(path):
                try:
                    img_surf = pygame.image.load(path).convert_alpha()
                    orig_w, orig_h = img_surf.get_size()
                    
                    if not target_size and not scale_factor and (orig_w > 100 or orig_h > 100):
                        scale_factor = 64 / orig_h
                        new_w = int(orig_w * scale_factor)
                        new_h = int(orig_h * scale_factor)
                        image = pygame.transform.scale(img_surf, (new_w, new_h))
                        print(f"[Auto-Scale] {key}: Reduzido de {orig_w}x{orig_h} para {new_w}x{new_h}")

                    elif scale_factor and isinstance(scale_factor, (int, float)):
                        new_w = int(orig_w * scale_factor)
                        new_h = int(orig_h * scale_factor)
                        image = pygame.transform.scale(img_surf, (new_w, new_h))
                    
                    elif target_size:
                        image = pygame.transform.scale(img_surf, target_size)
                    
                    else:
                        image = img_surf 
                        
                except Exception as e:
                    print(f"Erro ao carregar imagem {path}: {e}")

        # Fallback
        if image is None:
            final_size = target_size if target_size else (64, 64)
            if scale_factor and isinstance(scale_factor, (int, float)):
                sz = int(32 * scale_factor)
                final_size = (sz, sz)
                
            image = pygame.Surface(final_size, pygame.SRCALPHA)
            
            color = ENTITY_COLORS.get(color_key, (255, 255, 255))
            
            if shape == 'rect':
                image.fill(color)
                pygame.draw.rect(image, (255, 255, 255), (0,0,final_size[0],final_size[1]), 2)
            elif shape == 'circle':
                pygame.draw.circle(image, color, (final_size[0]//2, final_size[1]//2), final_size[0]//2)
                pygame.draw.circle(image, (255, 255, 255), (final_size[0]//2, final_size[1]//2), final_size[0]//2, 2)
            
        self.assets[cache_key] = image
        return image

def import_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)