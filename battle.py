class BattleMon:
    def __init__(self,pokemon,team_size):
        self.pokemon = pokemon
        self.hp = pokemon.hp / pokemon.max_hp
        self.items = pokemon.items
        self.status = None
        self.stat_stages = {"atk": 0, "def": 0, "spd": 0, "sp_atk": 0, "sp_def": 0}
        self.remaining_team = team_size
        
class BattleState:
    def __init__(self, player_mon, enemy_mon):
        self.player = player_mon
        self.enemy = enemy_mon
