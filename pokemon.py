from constants import non_movement,status_damage, pokemon_growth
import random
from ui import show_message,get_user_in,get_user_move
import json
from moves import Move
from leveling import pokemon_exps_to_level
with open("data/pokemon.json") as f:
    all_pokemon = json.load(f)
with open("data/moves.json") as f:
    all_moves = json.load(f)

STAT_EFFECTS = {"attack", "defense", "speed", "accuracy"}
PASSIVE_FLAGS = {
    "reflect-status":  "mirror_dust",
    "status-immunity": "status_immune",
    "no-miss":         "no_miss",
    "always-first":    "always_first",
    "ignore-type":     "ignore_type",
    "untouchable":     "untouchable",
    "berserker":       "berserker",
}
class Pokemon:
    def __init__(self,name,type,base_hp,hp,base_attack,
                 base_speed,base_defense,status, items,
                 exp,level,moves,evolves_at,evolves_into,rarity):
        self.name=name
        self.type=type
        self.rarity = rarity
        self.growth = pokemon_growth[rarity]
        #Base stats
        self.base_hp=base_hp
        self.base_attack=base_attack
        self.base_speed=base_speed
        self.base_defense=base_defense
        
        #Calculated Stats
        self.max_hp = ((2* base_hp * level)//100)+10
        self.attack=((2*base_attack*level)//100)+5
        self.defense=((2*base_defense*level)//100)+5
        self.speed=((2*base_speed*level)//100)+5
        self.hp = hp
        
        self.status = {}
        self.items = {}
        self.exp=exp
        self.level=level
        self.moves=moves
        self.evolves_at=evolves_at
        self.evolves_into=evolves_into
    
    @classmethod
    def from_data(cls,data,current_hp,level,exps,moves):
        return cls(
            name = data["name"],
            type=data["types"],
            base_hp=data["base_hp"],
            hp = current_hp,
            base_attack = data["base_attack"],
            base_defense = data["base_defense"],
            base_speed = data["speed"],
            status = {},
            items = {},    
            exp=exps,
            level=level,
            moves=moves,
            evolves_at=data["evolves_at"],
            evolves_into=data["evolves_into"],
            rarity = data["rarity"]
        )
    
    def to_dict(self):
        return {
            "name": self.name,
            "types": self.type,
            "base_hp": self.base_hp,
            "base_attack": self.base_attack,
            "base_defense": self.base_defense,
            "speed": self.base_speed,
            "hp": self.hp,
            "exp": self.exp,
            "level": self.level,
            "moves": [m.to_dict() for m in self.moves],
            "evolves_at": self.evolves_at,
            "evolves_into": self.evolves_into,
            "status": self.status,
            "items":self.items,
            "rarity":self.rarity
        }
    
    def is_fainted(self):
        if self.hp<=0:
            self.hp=0
            return 1
        return 0
    
    def take_damage(self,damage):
        self.hp-=damage
        if self.is_fainted():
            show_message(f"{self.name} has Fainted")
            return 0
        return 1
    
    def level_up(self):
        self.level += 1
        self.attack = ((2 * self.base_attack * self.level) // 100) + 5
        self.defense = ((2 * self.base_defense * self.level) // 100) + 5
        self.speed = ((2 * self.base_speed * self.level) // 100) + 5
        new_hp = ((2 * self.base_hp * self.level) // 100) + self.level + 10
        self.max_hp = new_hp
        self.hp = new_hp
        show_message(f"{self.name} grew to level {self.level}!")
        
    def gain_exp(self, amount):
        self.exp += amount
        show_message(f"{self.name} gained {amount} XP!")
        while True:
            exps_next = pokemon_exps_to_level(self.level, self.growth)
            if self.exp >= exps_next:
                self.exp -= exps_next
                self.level_up()
                self.check_move()
                if self.level == self.evolves_at:
                    self.evolve()
            else:
                break
        
    def evolve(self):
        if not self.evolves_into:
            return
        
        show_message(f"{self.name} is evolving...")
        
        
        evolved_data = all_pokemon[self.evolves_into]
        
        self.name = evolved_data["name"]
        self.type = evolved_data["types"]
        self.rarity = evolved_data["rarity"]
        self.growth = pokemon_growth[self.rarity]
        
        self.base_hp = evolved_data["base_hp"]
        self.base_attack = evolved_data["base_attack"]
        self.base_defense = evolved_data["base_defense"]
        self.base_speed = evolved_data["speed"]
        
        self.max_hp = ((2 * self.base_hp * self.level) // 100) + self.level + 10
        self.attack = ((2 * self.base_attack * self.level) // 100) + 5
        self.defense = ((2 * self.base_defense * self.level) // 100) + 5
        self.speed = ((2 * self.base_speed * self.level) // 100) + 5
        
        self.hp = self.max_hp
        
        self.evolves_at = evolved_data["evolves_at"]
        self.evolves_into = evolved_data["evolves_into"]
        
        show_message(f"Evolved into {self.name}!")
    
    def check_move(self):
        level = self.level
        for move in all_pokemon[self.name]["moves"]:
            if move["at_lvl"] == level:
                show_message(f"{self.name} wants to learn {move["name"]}")
                usr = get_user_in("Would you like to proceed(y/n)")
                if usr:
                    move = Move.from_data(all_moves[move["name"]])
                    if len(self.moves) == 4:
                        show_message(f"{self.name} already knows 4 moves. Will need to forget one.")
                        selected_move = get_user_move(self)
                        self.moves.remove(selected_move)
                        self.moves.append(move)
                    else:
                        self.moves.append(move)
                    show_message(f"{self.name} has learned a new move {move.name}!")                            
                else:
                    continue
                
                
        
    def can_move(self):
        if self.status:
            for name,turns in list(self.status.items()):
                if name in non_movement and (turns!=0 or turns==None):
                    if turns is not None:
                        self.status[name]-=1
                        if turns == 0:
                            self.remove_effect(name)
                    if non_movement[name] < random.random()*100:
                        return 1
                    return 0
        return 1
    
    def apply_effect_damage(self,status,opponent=None):
        run = 0
        for effect in list(status.keys()):
            if effect not in status_damage:
                continue
            run+=1
            if status[effect] !=0 or status[effect] is None:
                damage_amt = status_damage[effect]*self.max_hp
                if effect == "nightmare":
                    if "sleep" not in self.status:
                        damage_amt = 0
                if effect == "leech-seed":
                    opponent.hp += damage_amt
                    opponent.hp = min(opponent.hp,opponent.max_hp)
                show_message(f"{self.name} is affected by {effect}" if effect != "leech-seed" else f"{self.name}'s hp has been drained.")
                self.hp-=int(damage_amt)
                show_message(f"{damage_amt} has been dealt" if effect != "leech-seed" else f"")
                if status[effect] is not None:
                    status[effect]-=1
                if status[effect] == 0:
                    self.remove_effect(effect)
        if run:
            return 1
        return 0
            
    def remove_effect(self,status):
        self.status.pop(status)
        
    def show_stats(self):
        show_message(f"\n--- {self.name}'s Stats ---")
        show_message(f"Type: {self.type}")
        show_message(f"Current HP : {self.hp} / {self.max_hp}")
        show_message(f"Attack: {self.attack}")
        show_message(f"Defense: {self.defense}")
        show_message(f"Speed: {self.speed}")

    def add_item(self,item,effect,value,turns):
        self.items[item]=[effect,value,turns]
        return 1
    
    def remove_items(self,item):
        if len(self.items):
            self.items.pop(item)
            return 1
        return 0
    
    def apply_item(self, name, effect, value, turns, opponent=None):
        if effect == "hp":
            self.hp = min(self.hp + self.max_hp * value, self.max_hp)
            return

        if effect == "status":
            self.status = {}
            return

        if effect == "gamble":
            import random
            if random.random() < 0.5:
                self.hp = self.max_hp
                show_message(f"{self.name} was fully healed!")
            else:
                self.hp = 0
                show_message(f"{self.name} fainted from Soul Gamble!")
            return

        if effect == "steal-attack":
            if opponent:
                stolen = int(opponent.attack * value)
                opponent.attack -= stolen
                self.attack += stolen
                show_message(f"Stole {stolen} attack from {opponent.name}!")
            return

        if effect == "random-status":
            import random
            all_statuses = ["burn", "poison", "paralysis", "sleep", "freeze", "confusion"]
            picked = random.choice(all_statuses)
            if opponent:
                opponent.status[picked] = 3
                show_message(f"Chaos Shard inflicted {picked}!")
            return

        if effect in STAT_EFFECTS:
            setattr(self, effect, getattr(self, effect) * value)
            self.items[name] = [effect, value, turns]
            return

        if effect in PASSIVE_FLAGS:
            setattr(self, PASSIVE_FLAGS[effect], True)
            self.items[name] = [effect, value, turns]
            return


    def tick_items(self):
        for name, (effect, value, turns) in list(self.items.items()):
            if turns is None:
                continue
            turns -= 1
            if turns <= 0:
                if effect in STAT_EFFECTS:
                    current = getattr(self, effect)
                    setattr(self, effect, round(current / value))
                if effect in PASSIVE_FLAGS:
                    setattr(self, PASSIVE_FLAGS[effect], False)
                del self.items[name]
                show_message(f"Effect of {name} has worn off!")
            else:
                self.items[name] = [effect, value, turns]