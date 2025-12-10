import json
import os

class SaveManager:
    def __init__(self):
        self.file_path = 'data/save_data.json'
        self.data = self.load_data()
        
        # Definição dos Upgrades Disponíveis
        # key: identificador interno
        # name: nome na loja
        # cost: custo inicial
        # cost_inc: aumento de custo por nível
        # desc: descrição do efeito
        self.upgrades_info = {
            'max_hp': {'name': 'Matrícula VIP', 'cost': 100, 'cost_inc': 50, 'desc': '+10 Vida Inicial'},
            'damage': {'name': 'Material de Ponta', 'cost': 150, 'cost_inc': 100, 'desc': '+5% Dano Base'},
            'speed': {'name': 'Atleta da AAA', 'cost': 100, 'cost_inc': 50, 'desc': '+5% Velocidade'},
            'xp_gain': {'name': 'Mente Aberta', 'cost': 200, 'cost_inc': 100, 'desc': '+10% Ganho de XP'},
            'gold_gain': {'name': 'Bolsa Permanência', 'cost': 200, 'cost_inc': 100, 'desc': '+10% Créditos'}
        }

    def load_data(self):
        if not os.path.exists(self.file_path):
            return self.create_default_save()
        
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except:
            return self.create_default_save()

    def create_default_save(self):
        default_data = {
            "credits": 0,
            "upgrades": {
                "max_hp": 0,
                "damage": 0,
                "speed": 0,
                "xp_gain": 0,
                "gold_gain": 0
            }
        }
        self.save_game(default_data)
        return default_data

    def save_game(self, data=None):
        if data:
            self.data = data
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_credits(self, amount):
        self.data['credits'] += int(amount)
        self.save_game()

    def get_upgrade_cost(self, key):
        current_lvl = self.data['upgrades'].get(key, 0)
        base_cost = self.upgrades_info[key]['cost']
        inc = self.upgrades_info[key]['cost_inc']
        return base_cost + (current_lvl * inc)

    def buy_upgrade(self, key):
        cost = self.get_upgrade_cost(key)
        if self.data['credits'] >= cost:
            self.data['credits'] -= cost
            self.data['upgrades'][key] += 1
            self.save_game()
            return True
        return False