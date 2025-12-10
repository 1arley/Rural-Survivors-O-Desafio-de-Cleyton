import pygame
import random
from src.entities.enemy import Enemy

class WaveManager:
    def __init__(self, game):
        self.game = game
        
        self.spawn_timer = 0
        self.base_spawn_rate = 1000
        self.current_spawn_rate = self.base_spawn_rate
        
        self.events_triggered = {
            'banca': False,
            'coordenador': False,
            'reitoria': False
        }

    def spawn_boss(self, boss_key):
        if not self.events_triggered.get(boss_key, False):
            self.game.spawn_enemy(boss_key)
            self.events_triggered[boss_key] = True
            print(f"!!! EVENTO: {boss_key.upper()} APARECEU !!!")

    def update(self, current_time_ms):
        minutes = current_time_ms / 60000
        
        pool = []
        
        # 0-2 min
        if minutes < 2:
            self.current_spawn_rate = 1000 
            pool = ['lista_exercicio']
            if minutes > 1: pool.append('seminario')

        # 2-4 min
        elif minutes < 4:
            self.current_spawn_rate = 800
            pool = ['lista_exercicio', 'seminario', 'gato_campus']
            if minutes >= 3: self.spawn_boss('banca')

        # 4-6 min
        elif minutes < 6:
            self.current_spawn_rate = 600
            pool = ['seminario', 'gato_campus', 'onibus_lotado']
            if minutes >= 5: self.spawn_boss('coordenador')

        # 6-8 min
        elif minutes < 8:
            self.current_spawn_rate = 400
            pool = ['onibus_lotado', 'gato_campus', 'ead']

        # 7:00 - 7:30 HORDA
        if 7.0 <= minutes < 7.5:
            self.current_spawn_rate = 60 
            pool = ['lista_exercicio', 'gato_campus'] 

        # 8-10 min
        elif minutes >= 8:
            self.current_spawn_rate = 300
            pool = ['onibus_lotado', 'ead', 'seminario']
            
            if minutes >= 9.5: self.spawn_boss('reitoria')

        # --- CORREÇÃO AQUI ---
        # Usa o tempo de jogo controlado (current_time_ms) ao invés do tempo do PC (get_ticks)
        if pool and (current_time_ms - self.spawn_timer > self.current_spawn_rate):
            enemy_type = random.choice(pool)
            self.game.spawn_enemy(enemy_type)
            self.spawn_timer = current_time_ms