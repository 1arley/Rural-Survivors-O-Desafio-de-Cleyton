from src.weapons.weapon_projectile import ProjectileWeapon
from src.weapons.weapon_melee import MeleeWeapon
from src.weapons.weapon_aura import AuraWeapon

class WeaponController:
    def __init__(self, player, groups, balance_data):
        self.player = player
        self.groups = groups
        self.balance_data = balance_data
        self.weapons = [] # Lista de objetos Weapon ativos
        self.weapons_map = {} # Nome -> Objeto (para upgrades rápidos)

    def add_weapon(self, name):
        if name in self.weapons_map:
            self.weapons_map[name].upgrade()
        else:
            if name not in self.balance_data['weapons']:
                print(f"Erro: Arma '{name}' não encontrada no balance.json")
                return

            data = self.balance_data['weapons'][name]
            w_type = data.get('type', 'projectile')
            
            new_weapon = None
            if w_type == 'projectile':
                new_weapon = ProjectileWeapon(self.player, self.groups, data)
            elif w_type == 'melee':
                new_weapon = MeleeWeapon(self.player, self.groups, data)
            elif w_type == 'aura':
                new_weapon = AuraWeapon(self.player, self.groups, data)
            
            if new_weapon:
                self.weapons.append(new_weapon)
                self.weapons_map[name] = new_weapon
                print(f"Arma adicionada: {name} ({w_type})")

    def update(self):
        for weapon in self.weapons:
            weapon.update()