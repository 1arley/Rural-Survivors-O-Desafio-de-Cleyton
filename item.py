import pygame

class ExperienceOrb(pygame.sprite.Sprite):
    def __init__(self, pos, groups, value):
        super().__init__(groups)
        self.image = pygame.image.load('assets/gem.png').convert_alpha()
        # Deixei pequeno pra não atrapalhar
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.rect = self.image.get_rect(center=pos)
        self.value = value