import math
from constants import base_exp_yield,player_exp_sources,player_growth
from ui import show_message

def pokemon_exps_to_level(level, growth=1.0):
    if level <=20:
        return math.floor(growth * 50 * level ** 1.8)
    elif level <=50:
        return math.floor(growth * 80 * level ** 2.2)
    elif level <=75:
        return math.floor(growth * 120 * level ** 2.8)
    else:
        return math.floor(growth * 200 * level ** 2.8)
    
def pokemon_exps_to_next_level(level, growth=1.0):
    return pokemon_exps_to_level(level+1,growth) - pokemon_exps_to_level(level,growth)

def player_exps_to_level(level,class_growth=1.0):
    if level <= 10:
        return math.floor(class_growth * 200 * level ** 1.5)
    elif level <=30:
        return math.floor(class_growth * 500 * level ** 2.0)
    elif level <=60:
        return math.floor(class_growth * 1000 * level ** 2.5)
    else:
        return math.floor(class_growth * 2000 * level ** 3.0)
    
def player_exps_to_next_level(level,growth=1.0):
    return player_exps_to_level(level+1,growth) - player_exps_to_level(level,growth)


def level_gap_modifier(attacker_level, defender_level):
    gap = defender_level - attacker_level
    if gap >= 10:    
        return 1.5    
    if gap >= 5:     
        return 1.2    
    if gap >= -5:    
        return 1.0    
    if gap >= -10:   
        return 0.7    
    return 0.4                     

def calculate_base_exp_yield(defeated,attacker):
    defeated_pokemon = getattr(defeated, "pokemon", defeated)
    base = base_exp_yield[defeated_pokemon.rarity]
    raw = math.floor(base * (defeated_pokemon.level / 5))
    modifier = level_gap_modifier(attacker.level, defeated_pokemon.level)
    return math.floor(raw * modifier)


def award_player(player, source):
    amount = player_exp_sources[source]
    
    scaled = math.floor(amount * (1 + player.level * 0.05))
    
    return scaled
    
    
    
def distribute_exps(pokemons,defeated):
    eligible = [p for p in pokemons if not p.pokemon.is_fainted()]
    
    if not eligible:
        return 0
    
    share_penalty = 0.7 if len(eligible) > 1 else 1.0
    
    for pokemon in eligible:
        total_exps = calculate_base_exp_yield(pokemon,defeated)
        each_exps = math.floor((total_exps / len(eligible)) * share_penalty)
        pokemon.pokemon.gain_exp(each_exps)


def player_level_up(player,source):
    gained = award_player(player,source)
    player.gain_exp(gained)