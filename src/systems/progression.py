class EvolutionSystem:
    def __init__(self):
        # Definição das Receitas: (Arma, Passivo) -> Evolução
        self.recipes = {
            ('Caderno', 'Calculadora'): 'TCC Completo',
            ('Caneta', 'Cafe'): 'Caneta Profissional'
        }

    def check_evolution(self, player):
        """
        Retorna o nome da arma evoluída se as condições forem atendidas,
        caso contrário retorna None.
        """
        possible_evolutions = []

        # Mapeia os passivos do player e seus níveis para busca rápida
        player_passives = {p['name']: p['level'] for p in player.passives}

        for weapon_name, weapon_data in player.weapon_controller.weapons_data.items():
            # Condição 1: Arma Nível 8
            if weapon_data['lvl'] >= 8:
                
                # Procura receitas para esta arma
                for (recipe_weapon, recipe_passive), result in self.recipes.items():
                    # Normaliza nomes (se necessário, ou use IDs consistentes)
                    if recipe_weapon.lower() == weapon_name.lower():
                        
                        # Condição 2: Passivo Nível 6
                        # Verifica se o player tem o passivo necessário no nível correto
                        if recipe_passive in player_passives:
                            if player_passives[recipe_passive] >= 6:
                                possible_evolutions.append(result)

        if possible_evolutions:
            return possible_evolutions[0] # Retorna a primeira encontrada
        return None