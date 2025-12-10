import random

MAX_WEAPON_SLOTS = 4
MAX_PASSIVE_SLOTS = 4

class UpgradeManager:
    def __init__(self, balance_data):
        self.data = balance_data

    def get_random_options(self, player, weapon_controller, count=3):
        possible_picks = []
        
        # Inventários Atuais
        current_weapons = weapon_controller.weapons_map
        current_passives = player.inventory # {'key': lvl}
        
        weapons_full = len(current_weapons) >= MAX_WEAPON_SLOTS
        passives_full = len(current_passives) >= MAX_PASSIVE_SLOTS

        # --- 1. CHECAR EVOLUÇÕES (Prioridade Máxima) ---
        # Se tiver um baú (futuro) ou sorteio especial, a evolução aparece aqui.
        # Por enquanto, vamos colocar na roleta normal se cumprir requisitos.
        for key, weapon in current_weapons.items():
            if weapon.lvl >= 8:
                evo_data = weapon.data.get('evolution')
                if evo_data:
                    req_passive = evo_data['passive']
                    result_weapon = evo_data['result']
                    
                    # Se tem o passivo necessário E ainda não tem a arma evoluída
                    if req_passive in current_passives and result_weapon not in current_weapons:
                        # Adiciona a Evolução como opção
                        info = self.data['weapons'][result_weapon]
                        possible_picks.append({
                            'type': 'evolution', # Tipo especial
                            'key': result_weapon, # Nova arma
                            'base_key': key,      # Arma antiga para substituir
                            'display_name': "EVOLUÇÃO: " + info['name'],
                            'desc': info['desc'],
                            'lvl': 1,
                            'icon': info.get('image', 'proj')
                        })

        # --- 2. PROCESSAR ARMAS NORMAIS ---
        for key, info in self.data['weapons'].items():
            # Pula se for uma arma evoluída (elas não aparecem na roleta normal)
            # Assumimos que armas evoluídas não têm campo 'evolution' ou são marcadas
            # Simplificação: Se a arma não está no inventário e é uma evolução de alguém, pula.
            is_evolution = False
            for w in self.data['weapons'].values():
                if w.get('evolution', {}).get('result') == key:
                    is_evolution = True
                    break
            
            # Se já tem a arma
            if key in current_weapons:
                w = current_weapons[key]
                if w.lvl < 8: # Max level normal
                    possible_picks.append({
                        'type': 'weapon', 'key': key,
                        'display_name': info['name'], 'desc': info['desc'],
                        'lvl': w.lvl, 'icon': info.get('image', 'proj')
                    })
            # Se não tem e não é evolução e tem espaço
            elif not is_evolution and not weapons_full:
                possible_picks.append({
                    'type': 'weapon', 'key': key,
                    'display_name': info['name'], 'desc': info['desc'],
                    'lvl': 0, 'icon': info.get('image', 'proj')
                })

        # --- 3. PROCESSAR PASSIVOS ---
        for key, info in self.data['passives'].items():
            lvl = current_passives.get(key, 0)
            if (lvl > 0 and lvl < 5) or (lvl == 0 and not passives_full):
                possible_picks.append({
                    'type': 'passive', 'key': key,
                    'display_name': info['name'], 'desc': info['desc'],
                    'lvl': lvl, 'data': info
                })

        if not possible_picks:
            return [{'type': 'passive', 'key': 'marmita', 'display_name': 'Cura Extra', 'desc': 'Recupera 30 HP', 'lvl': 99, 'data': {'stat': 'max_hp', 'value': 0}}] # Cura placeholder
            
        # Retorna até 'count' opções
        # (Idealmente dar peso maior para armas que você já tem)
        return random.sample(possible_picks, min(len(possible_picks), count))