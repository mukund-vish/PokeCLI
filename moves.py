import random
from constants import type_chart
from ui import show_message
class Move:
    def __init__(self, name, type, power, pp, accuracy, target, damage_class, effect_chance,
                 status_effect, status_effect_chance, move_category, crit_rate,
                 drain, flinch_chance, healing, max_hits, min_hits, max_turns,
                 min_turns, stat_chance, stat_changes):
        self.name = name
        self.type = type
        self.power = power
        self.pp = pp
        self.max_pp = pp
        self.accuracy = accuracy
        self.target = target
        self.damage_class = damage_class
        self.effect_chance = effect_chance
        self.status_effect = status_effect
        self.status_effect_chance = status_effect_chance
        self.move_category = move_category
        self.crit_rate = crit_rate
        self.drain = drain
        self.flinch_chance = flinch_chance
        self.healing = healing
        self.max_hits = max_hits
        self.min_hits = min_hits
        self.max_turns = max_turns
        self.min_turns = min_turns
        self.stat_chance = stat_chance
        self.stat_changes = stat_changes
    
    @classmethod
    def from_data(cls,data):
        return cls(
            name = data["name"],
            type=data["type"],
            power=data["power"],
            pp = data["pp"],
            accuracy = data["accuracy"],
            target = data["target"],
            damage_class = data["damage_class"],
            effect_chance = data["effect_chance"],
            status_effect = data["status_effect"],
            status_effect_chance = data["status_effect_chance"],
            move_category = data["move_category"],
            crit_rate = data["crit_rate"],
            drain = data["drain"],
            flinch_chance = data["flinch_chance"],
            healing = data["healing"],
            max_hits = data["max_hits"],
            min_hits = data["min_hits"],
            max_turns = data["max_turns"],
            min_turns = data["min_turns"],
            stat_chance = data["stat_chance"],
            stat_changes = data["stat_changes"]
        )
    
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type,
            "power": self.power,
            "pp": self.pp,
            "max_pp":self.max_pp,
            "accuracy": self.accuracy,
            "target": self.target,
            "damage_class": self.damage_class,
            "effect_chance" : self.effect_chance,
            "status_effect":self.status_effect,
            "status_effect_chance":self.status_effect_chance,
            "move_category":self.move_category,
            "crit_rate":self.crit_rate,
            "drain":self.drain,
            "flinch_chance":self.flinch_chance,
            "healing":self.healing,
            "max_hits":self.max_hits,
            "min_hits":self.min_hits,
            "max_turns":self.max_turns,
            "min_turns":self.min_turns,
            "stat_chance":self.stat_chance,
            "stat_changes":self.stat_changes
        }
    def use(self):
        if self.pp:
            self.pp-=1
            return 1
        show_message(f"{self.name} has no PP left")
        return 0
    
    
    def apply_effect(self,attacker,defender):
        if self.target == "user":
            target = attacker
        else:
            target = defender
        
        if self.status_effect!="none":
            if self.status_effect_chance >= random.randint(1,100):
                e_status = self.status_effect
                if self.min_turns is not None:
                    s_turn = random.randint(self.min_turns,self.max_turns)
                else:
                    s_turn = None
                target.status[e_status] = s_turn
                show_message(f"{target.name} is now {self.status_effect}")
        
        if self.stat_changes:
            if random.random()*100 <= self.stat_chance:
                for stat,change in self.stat_changes.items():
                    if stat == "special-attack":
                        stat = "attack"
                    elif stat == "special-defense":
                        stat = "defense"
                    current = getattr(target,stat)
                    setattr(target,stat,current+change)
                    show_message(f"{target.name}'s {stat} {'rose' if change > 0 else 'fell'}!")
    
    
    def get_damage(self, attacker, defender):
        if self.power is None:
            return 0

        if self.accuracy is not None:
            if random.random()*100 > self.accuracy:
                show_message(f"{attacker.name}'s misses the attack")
                return 0

        effectiveness = 1
        for d_type in defender.type:
            effectiveness *= type_chart.get(self.type, {}).get(d_type, 1)

        if effectiveness == 0:
            show_message("It had no effect!")
            return 0
        elif effectiveness < 1:
            show_message("It is not that effective")
        elif effectiveness > 1:
            show_message("It proves to be super effective!")

        crit_stages = {0: 6.25, 1: 12.5, 2: 50, 3: 100}
        crit_chance = crit_stages.get(self.crit_rate, 6.25)
        is_crit = random.random()*100 <= crit_chance
        crit_multiplier = 1.5 if is_crit else 1

        level = attacker.level

        base_damage = ((2 * level / 5 + 2) * self.power * attacker.attack / defender.defense) / 50 + 2
        damage = base_damage * effectiveness * crit_multiplier

        if self.min_hits is not None:
            hits = random.randint(self.min_hits, self.max_hits)
            total_damage = sum(int(damage) for _ in range(hits))
            show_message(f"{self.name} hit {hits} time(s)")
            return total_damage

        return int(damage)
                