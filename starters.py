import json
from move_selector import select_move
from pokemon import Pokemon
from constants import starters_id,pokemon_growth
from leveling import pokemon_exps_to_level
def starter_list():
    starters_data ={}
    with open("data/pokemon.json") as f:
        database = json.load(f)
    
    for i in database:
        if database[i]["id"] in starters_id:
            starters_data[i]=database[i]
    return starters_data

def selected_pokemon(pokemon):
    poke_moves = select_move(pokemon["moves"],5)
    return Pokemon.from_data(pokemon,((2* pokemon["base_hp"] * 5)//100)+10,5,pokemon_exps_to_level(5,pokemon_growth[pokemon["rarity"]]),poke_moves)
