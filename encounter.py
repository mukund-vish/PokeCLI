import json
import random
from move_selector import select_move
from pokemon import Pokemon
from ui import show_message, encounter_method, get_user_in, capsule_quantity
from constants import items as drop_items,pokemon_growth
from leveling import pokemon_exps_to_level
bush_rarities = {
    "green": {
        "rarities": ["common", "uncommon"],
        "weights": [60, 40]
    },
    "blue": {
        "rarities": ["uncommon", "rare"],
        "weights": [55, 45]
    },
    "red": {
        "rarities": ["rare", "mythical", "legendary"],
        "weights": [55, 30, 15]
    }
}

catch_rates = {
    "common":    70,
    "uncommon":  50,
    "rare":      30,
    "mythical":  10,
    "legendary": 5
}
kill_rates = {
    "common":    55,   
    "uncommon":  45,
    "rare":      30,
    "mythical":  15,
    "legendary": 5     
}

with open("data/pokemon.json") as f:
        poke_database = json.load(f)
with open("data/rarities.json") as f:
        rarity_database = json.load(f)
def wild_encounter(player_level, bush_type,player_using_items, items):
    bush = bush_rarities[bush_type]

    for _ in range(10):
        poke_lvl = random.randint(max(1, player_level - 5), player_level + 5)
        if len(player_using_items) > 0 and player_using_items["item"]=="rarity-charm":
            rarity = random.choices(["rare","mythical","legendary"], weights=[50,30,20])[0]
            items["rarity-charm"]-=1
            player_using_items.clear()
        else:
            rarity = random.choices(bush["rarities"], weights=bush["weights"])[0]
        if len(player_using_items) > 0 and player_using_items["item"]=="lure-stone":
            poke_id = random.choice(rarity_database["rare"])
            items["lure-stone"]-=1
            player_using_items.clear()
        else:
            poke_id = random.choice(rarity_database[rarity])
        
        

        pokemon_name = None
        pokemon_data = None
        for name, data in poke_database.items():
            if data["id"] == poke_id and data["min_level"] <= poke_lvl:
                pokemon_name = name
                pokemon_data = data
                break

        if pokemon_name is None:
            continue

        poke_moves = select_move(pokemon_data["moves"], poke_lvl)
        hp = ((2 * pokemon_data["base_hp"] * poke_lvl) // 100) + 10
        exp = pokemon_exps_to_level(poke_lvl, pokemon_growth[pokemon_data["rarity"]])
        return Pokemon.from_data(pokemon_data, hp, poke_lvl, exp, poke_moves)

    raise RuntimeError("Could not generate a valid wild pokemon after 10 attempts")

def start_encounter(player,pokemon,items,player_using_items):
    if len(player_using_items) > 0 and player_using_items["item"]=="flee-freeze":
        turns = 5 + random.randint(1,10)
        items["flee-freeze"]-=1
        player_using_items.clear()
    else:        
        turns = random.randint(1,10)
    while(turns):
        play_mode = encounter_method()
        if play_mode == 3:
            show_message("You have run away from the encounter.")
            return 0
        result = start_play(player,play_mode,items,pokemon,poke_database)
        if result == -1:
            turns-=1
            if play_mode == 1:
                if turns:
                    show_message("You still have a chance.....")
                    continue
                break
            if play_mode == 2:
                player.lose_life()
                show_message(f"Lives remaining {player.lives}")
                return 0
        if result:
            if play_mode == 1:
                return 1
            else:
                return 0
    return 0
            
        

def start_play(player,play_mode,items,pokemon,database):
    if play_mode:
        if play_mode==1:
            return attempt_catch(player,items,pokemon,database)
        if play_mode==2:
            return attempt_kill(player,pokemon,database)



def attempt_catch(player,items,pokemon,database):
    if items["catch_balls"]:
                does_charge = attempt_charge(items)
                if does_charge :
                    return 1
                items["catch_balls"]-=1
                poke_catch_rate = catch_rates[database[pokemon.name]["rarity"]]
                if random.random()*100 < poke_catch_rate:
                    show_message(f"{pokemon.name} caught.")
                    return 1
                show_message("Pokemon broke free....")
                return -1
    else:
                show_message("You have no catch balls left.")
                show_message("Hence, you cannot catch this pokemon.")
                option_in = get_user_in("Would you like to switch to option 2.(y/n)")
                if option_in:
                    return attempt_kill(player,pokemon,database)

def attempt_kill(player,pokemon,database):
    poke_rarity = database[pokemon.name]["rarity"]
    poke_kill_rate = kill_rates[poke_rarity]
    if random.random()*100 < poke_kill_rate:
        show_message(f"{pokemon.name} has been killed by you.")
        possible_items = get_drop_reward(poke_rarity)
        reward_drop(player,pokemon,possible_items)
        return 1
    show_message(f"You been killed by {pokemon.name}")
    return -1

def reward_drop(player,pokemon, possible_items):
    how_many = random.randint(1,3)
    given = 0
    for item in possible_items:
        if given < how_many:
            quantity = random.randint(1,3)
            player.add_item(item,quantity)
            show_message(f"{pokemon.name} has dropped {item} *{quantity}")
            given+=1
        else:
            break
    return 1

def get_drop_reward(poke_rarity):
    if poke_rarity == "common":
        possible_items = [possible for possible in drop_items if drop_items[possible]["price"] and drop_items[possible]["price"]<400]
    elif poke_rarity == "uncommon":
        possible_items = [possible for possible in drop_items if drop_items[possible]["price"] and drop_items[possible]["price"]>400]
    elif poke_rarity == "rare":
        possible_items = [possible for possible in drop_items if not(drop_items[possible]["price"]) and possible!="legendary-aura"]
    elif poke_rarity == "legendary":
        possible_items = [possible for possible in drop_items]
    return possible_items



def attempt_charge(player_items):
    if player_items["capsule"]:
        user = get_user_in("Would you like to charge the catch ball (y/n)")
        if user:
            quantity = capsule_quantity()
            player_items["capsule"]-=quantity
            show_message(f"Remaining capsules are {player_items["capsule"]}")
            increase_rates = quantity * 10
            for rates in catch_rates:
                catch_rates[rates]*=increase_rates
            return 1
        return 0
    return 0



def get_trainer_pokemon(max_lvl,trainer_level):
    poke_level = random.randint(max_lvl,trainer_level+1)
    pokemons = []
    for pokemon in poke_database:
        if poke_database[pokemon]["rarity"] not in ["mythical","legendary"] and poke_database[pokemon]["min_level"]<=poke_level:
            pokemons.append(pokemon)
    
    selected = random.choice(pokemons)
    selected_moves = select_move(poke_database[selected]["moves"],poke_level)
    choosen = Pokemon.from_data(poke_database[selected],((2* poke_database[selected]["base_hp"] * poke_level)//100)+10,poke_level,poke_level*100,selected_moves)
    return choosen
    