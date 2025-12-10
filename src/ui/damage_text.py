import pygame
import random
from settings import *
from src.utils.helpers import AssetManager

class DamageText(pygame.sprite.Sprite):
    def __init__(self, pos, value, groups, is_critical=False):
        super().__init__(groups)
        self.assets = AssetManager()
        
        # Configuração Visual
        if isinstance(value, str):
            # Texto (Esquiva, Block)
            text = value
            color = (100, 255, 255) 
            size = 20
            self.speed = 1
        else:
            # Número (Dano)
            val_int = int(value)
            text = str(val_int)
            
            if is_critical:
                color = (255, 50, 50) # Vermelho Sangue
                size = 32             # Fonte Grande
                text += "!"           # Ênfase
                self.speed = 3        # Sobe mais rápido (explosão)
            else:
                color = (255, 255, 255) 
                size = 18
                if val_int > 20: 
                    color = (255, 255, 0) # Amarelo para hits fortes normais
                    size = 22
                self.speed = 1.5

        # Carrega a fonte
        font = self.assets.load_font(size)
        
        # Renderiza texto e Borda
        self.image = font.render(text, True, color)
        outline = font.render(text, True, (0,0,0))
        
        # Cria superfície composta
        w, h = self.image.get_size()
        final_surf = pygame.Surface((w + 2, h + 2), pygame.SRCALPHA)
        # Desenha borda (4 direções)
        final_surf.blit(outline, (0, 1))
        final_surf.blit(outline, (2, 1))
        final_surf.blit(outline, (1, 0))
        final_surf.blit(outline, (1, 2))
        # Desenha texto principal
        final_surf.blit(self.image, (1, 1))
        
        self.image = final_surf
        self.rect = self.image.get_rect(center=pos)
        
        # Movimento
        self.pos = pygame.math.Vector2(self.rect.topleft)
        # Variação horizontal maior para críticos
        spread = 1.5 if is_critical else 0.5
        random_x = random.uniform(-spread, spread)
        self.direction = pygame.math.Vector2(random_x, -1) 
        
        self.alpha = 255
        self.timer = 0
        self.life_time = 800 # ms

    def update(self, dt):
        self.pos += self.direction * self.speed
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        # Gravidade leve no texto (efeito de pulo)
        self.speed = max(0.5, self.speed * 0.95)
        
        self.timer += dt * 1000
        if self.timer > self.life_time / 2:
            self.alpha -= 10
            self.alpha = max(0, self.alpha)
            self.image.set_alpha(self.alpha)
            
        if self.timer >= self.life_time:
            self.kill()