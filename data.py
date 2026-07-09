import requests
import json
import os
import time
# Pokemon Data

def fetch_pokemon(id):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = response.json()
    
    #ID of the pokemon
    poke_id = id
    # Name of the Pokemon
    poke_name=data["name"]
    
    # Stats of the Pokemon
    stats = {s["stat"]["name"] : s["base_stat"] for s in data["stats"]}
    
    #Type(s) of the Pokemon
    types = [t["type"]["name"] for t in data["types"]]
    
    moves=[]
    seen = set()
    move_lvl={}
    for move in data["moves"]:
        
        for details in move["version_group_details"]:
            
            learn_method = details["move_learn_method"]["name"]
            lvl = 0
            move_name=move["move"]["name"]
            
            if (move_name,learn_method) not in seen:
                if learn_method=="level-up":
                    lvl = details["level_learned_at"]
                    if move_name not in move_lvl:
                        move_lvl[move_name]=lvl
                    else:
                        move_lvl[move_name]=min(move_lvl[move_name],lvl)
                else:
                    moves.append({
                        "name":move_name,
                        "method":learn_method,
                        "at_lvl":lvl
                    })
                    seen.add((move_name,learn_method))
    for name,lvl in move_lvl.items():
        moves.append({
            "name":name,
            "at_lvl":lvl
        })
                
    s_response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{id}")
    species_data = s_response.json()
    
    
    capture_rate = species_data["capture_rate"]
    
    if species_data["is_legendary"]:
        rarity = "legendary"
    elif species_data["is_mythical"]:
        rarity = "mythical"
    elif capture_rate >= 200:
        rarity = "common"
    elif capture_rate >= 120:
        rarity = "uncommon"
    else:
        rarity = "rare"
    
    chain_url = species_data["evolution_chain"]["url"]
    chain_response = requests.get(chain_url)
    chain_data = chain_response.json()
    chain = chain_data["chain"]
    evolves_at,evolves_into=walk(chain,poke_name)
    min_level = walk_for_min(chain,poke_name) or 1
    
    return {
    "id":poke_id,
    "name": poke_name,
    "types": types,
    "rarity" : rarity,
    "base_hp": stats["hp"],
    "base_attack": stats["attack"],
    "base_defense": stats["defense"],
    "speed": stats["speed"],
    "moves": sorted(moves, key=lambda x: x["at_lvl"]),
    "evolves_at": evolves_at,
    "evolves_into": evolves_into,
    "min_level":min_level
    }
    

def walk(chain, target_name):
    current = chain["species"]["name"]
    
    if current == target_name:
        if len(chain["evolves_to"]) == 0:
            return None, None
        next_pokemon = chain["evolves_to"][0]
        
        if len(next_pokemon["evolution_details"]) == 0:
            return None, None
            
        evolves_into = next_pokemon["species"]["name"]
        details = next_pokemon["evolution_details"][0]
        
        trigger = details["trigger"]["name"]
        if trigger == "level-up":
            evolves_at = details["min_level"]
        elif trigger == "use-item":
            evolves_at = details["item"]["name"]
        else:
            evolves_at = trigger
        return evolves_at, evolves_into
    
    for branch in chain["evolves_to"]:
        result = walk(branch, target_name)
        if result != (None, None):
            return result
    
    return None, None

def walk_for_min(chain, target_name, parent_evolve_at=1):
    current = chain["species"]["name"]
    
    if current == target_name:
        return parent_evolve_at 
    
    for branch in chain["evolves_to"]:
        details = branch["evolution_details"]
        if details and details[0]["trigger"]["name"] == "level-up":
            evolve_lvl = details[0]["min_level"] or 1
        else:
            evolve_lvl = parent_evolve_at 
        
        result = walk_for_min(branch, target_name, evolve_lvl)
        if result is not None:
            return result
    
    return None

def get_pokemon(id):
    pokemon=fetch_pokemon(id)
    os.makedirs("data", exist_ok=True)
    if os.path.exists("data/pokemon.json"):
        with open("data/pokemon.json") as f:
            database = json.load(f)
    else:
        database = {}
        
    
    poke_name=pokemon["name"]
    database[poke_name] = pokemon

    with open("data/pokemon.json", "w") as f:
        json.dump(database, f, indent=4)
        

# for i in range(1,1026):
#     print(f"Fetching the Data of pokemon {i}")
#     get_pokemon(i)
#     print(f"\n Done. \n\n")
#     time.sleep(0.5)

# Move Data


def fetch_move(move):
    

    m_request = requests.get(f"https://pokeapi.co/api/v2/move/{move}")
    move_data = m_request.json()
    
    move_name = move
    move_type = move_data["type"]["name"]
    move_power = move_data["power"]
    move_accuracy = move_data["accuracy"]
    move_pp = move_data["pp"]
    move_target = move_data["target"]["name"]
    damage_class = move_data["damage_class"]["name"]
    effect_chance = move_data["effect_chance"]
    
    move_meta = move_data["meta"]
    if move_meta is None:
        return {
            "name": move_name,
            "type": move_type,
            "power": move_power,
            "pp": move_pp,
            "max_pp": move_pp,
            "accuracy": move_accuracy,
            "target": move_target,
            "damage_class": damage_class,
            "effect_chance": effect_chance,
            "status_effect": "none",
            "status_effect_chance": 0,
            "move_category": "none",
            "crit_rate": 0,
            "drain": 0,
            "flinch_chance": 0,
            "healing": 0,
            "max_hits": None,
            "min_hits": None,
            "max_turns": None,
            "min_turns": None,
            "stat_chance": 0,
            "stat_changes": {}
        }
    
    status_effect=move_meta["ailment"]["name"] if move_meta["ailment"] else "none"
    status_effect_chance=move_meta["ailment_chance"]
    move_category=move_meta["category"]["name"]
    crit_rate = move_meta["crit_rate"]
    drain = move_meta["drain"]
    flinch_chance = move_meta["flinch_chance"]
    healing = move_meta["healing"]
    max_hits = move_meta["max_hits"]
    min_hits = move_meta["min_hits"]
    max_turns = move_meta["max_turns"]
    min_turns = move_meta["min_turns"]
    stat_chance = move_meta["stat_chance"]
    
    stat_changes = {}
    for stat in move_data["stat_changes"]:
        stat_changes[stat['stat']['name']] = stat['change']
    
    return {
    "name": move_name,
    "type": move_type,
    "power": move_power,
    "pp": move_pp,
    "max_pp": move_pp,
    "accuracy": move_accuracy,
    "target" : move_target,
    "damage_class": damage_class,
    "effect_chance": effect_chance,
    "status_effect": status_effect,
    "status_effect_chance": status_effect_chance,
    "move_category": move_category,
    "crit_rate": crit_rate,
    "drain": drain,
    "flinch_chance": flinch_chance,
    "healing": healing,
    "max_hits": max_hits,
    "min_hits": min_hits,
    "max_turns": max_turns,
    "min_turns": min_turns,
    "stat_chance": stat_chance,
    "stat_changes": stat_changes
}
    
    
def get_move(move):
    print(move,"move is fetching")
    move=fetch_move(move)
    os.makedirs("data", exist_ok=True)
    if os.path.exists("data/moves.json"):
        with open("data/moves.json") as f:
            m_database = json.load(f)
    else:
        m_database = {}
        
    
    move_name=move["name"]
    m_database[move_name] = move

    with open("data/moves.json", "w") as f:
        json.dump(m_database, f, indent=4)


def build_rarity_index():
    with open("data/pokemon.json") as f:
        database = json.load(f)
    
    rarities = {
        "common": [],
        "uncommon": [],
        "rare": [],
        "mythical": [],
        "legendary": []
    }
    
