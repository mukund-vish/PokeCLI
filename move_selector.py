from data import get_move
from moves import Move
import json 
import random

def select_move(pokemon_moves,level):
    learnable_moves = [moves for moves in pokemon_moves if moves["at_lvl"]<=level and moves["at_lvl"]>0]
    with open("data/moves.json") as f:
        moves_db = json.load(f)
    
    damage = []
    status = []
    
    for move in learnable_moves:
        name = move["name"]
        if name not in moves_db:
            get_move(name)
            with open("data/moves.json") as f:
                moves_db = json.load(f)
        
        if moves_db[name]["damage_class"]=="status":
            status.append(moves_db[name])
        else:
            damage.append(moves_db[name])
            
    random.shuffle(status)
    random.shuffle(damage)
    
    selected = []
    if damage:
        selected.append(damage[0]["name"])
        remaining = damage[1:]+status
    else:
        remaining = status
    for move in remaining:
        if len(selected)>=4:
            break
        selected.append(move["name"])
    
    final_moves = []
    for move in selected:
        final_moves.append(Move.from_data(moves_db[move]))

    return final_moves