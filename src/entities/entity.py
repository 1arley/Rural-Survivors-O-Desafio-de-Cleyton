import pygame
import math
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        # --- SISTEMA DE ANIMAÇÃO ---
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = [] # Lista de imagens para animação
        self.original_image_anim = None # Guarda a imagem base para rotação procedural
        
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2() 

    def set_hitbox(self):
        """Define uma hitbox baseada nos pés da entidade."""
        if hasattr(self, 'rect'):
            width = self.rect.width * 0.6   
            height = self.rect.height * 0.3 
            self.hitbox = pygame.Rect(0, 0, width, height)
            self.hitbox.midbottom = self.rect.midbottom
            self.hitbox.y -= 1
            self.pos = pygame.math.Vector2(self.hitbox.center)
            
            # Salva imagem original para animação procedural se não tiver frames
            if not self.frames:
                self.original_image_anim = self.image.copy()

    def animate(self, dt):
        """Gerencia animação de andar."""
        is_moving = self.direction.magnitude() > 0

        # CASO 1: Tem frames de animação (Spritesheet)
        if self.frames:
            if is_moving:
                self.frame_index += self.animation_speed
                if self.frame_index >= len(self.frames):
                    self.frame_index = 0
                self.image = self.frames[int(self.frame_index)]
            else:
                self.image = self.frames[0] # Frame parado
        
        # CASO 2: Não tem frames (Animação Procedural / Wobble)
        elif self.original_image_anim:
            if is_moving:
                # Cria um efeito de "gingado" usando seno e o tempo
                wobble_angle = sin(pygame.time.get_ticks() * 0.015) * 5 # +/- 5 graus
                self.image = pygame.transform.rotate(self.original_image_anim, wobble_angle)
                # Recentraliza o rect pois rotação muda o tamanho
                self.rect = self.image.get_rect(center=self.hitbox.center)
                self.rect.midbottom = self.hitbox.midbottom # Mantém os pés no chão
            else:
                # Reseta rotação
                self.image = self.original_image_anim
                self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.pos.x += self.direction.x * speed
        self.hitbox.centerx = round(self.pos.x)
        self.collision('horizontal')
        
        self.pos.y += self.direction.y * speed
        self.hitbox.centery = round(self.pos.y)
        self.collision('vertical')
        
        self.rect.midbottom = self.hitbox.midbottom

    def collision(self, direction):
        pass