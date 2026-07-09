from constants import type_chart
from ui import show_message
def score_pokemon(pokemon,enemy_pokemon,weights):
    effectiveness = 1
    if pokemon.hp :
        hp_score = enemy_pokemon.hp
        for type in pokemon.type:
            for e_type in enemy_pokemon.pokemon.type:
                effectiveness*=type_chart[type].get(e_type,1.0)
        best_move_effectiveness = 0
        for move in pokemon.moves:
            move_eff = 1
            for e_type in enemy_pokemon.pokemon.type:
                move_eff *= type_chart.get(move.type, {}).get(e_type, 1)
            if move_eff > best_move_effectiveness:
                best_move_effectiveness = move_eff
        return (
            (weights["effectiveness"] * effectiveness) +
              (weights["hp"]            * hp_score) +
              (weights["coverage"]      * best_move_effectiveness)
        )
    return 0

def score_move(move,battle_state,weights):
    player = battle_state.player
    enemy = battle_state.enemy
    
    effectiveness = 1
    
    for e_type in enemy.pokemon.type:
        effectiveness *= type_chart.get(move.type, {}).get(e_type,1)
        
    if move.power is None:
        damage = 0
    else:
        damage = move.power * player.pokemon.attack / enemy.pokemon.defense * effectiveness
    
    enemy_remaining_hp = enemy.hp * enemy.pokemon.max_hp
    kO_bonus = 1.5 if enemy_remaining_hp <= damage else 1.0
    
    accuracy = move.accuracy if move.accuracy is not None else 0
    
    status = 0
    status = move.status_effect_chance if not enemy.pokemon.status and move.status_effect != "none" else 0
    
    pp_penalty = 0 if move.pp > 1 else -100
    
    return ( 
            weights["damage"] * damage * kO_bonus + weights["status"] * status +
            weights["accuracy"] * accuracy + pp_penalty
            )


def pick_move(battle_state,weights):
    all_moves = battle_state.enemy.pokemon.moves
    usable = [m for m in all_moves if m.pp > 0]
    if not(usable):
        return None
    best_move = None
    best_score = -1
    
    for m in usable:
        score = score_move(m, battle_state,weights)
        if  score> best_score:
            best_score = score
            best_move = m
    return best_move


def run_move(move,battle_state,weights):
    player = battle_state.player
    enemy = battle_state.enemy
    first = None
    second = None
    first_move = None
    second_move = None
    t=0
    enemy_move = pick_move(battle_state,weights)
    player_move = move
    
    if player_move is None:
        if enemy_move and not player.pokemon.is_fainted():
            damage = enemy_move.get_damage(enemy.pokemon, player.pokemon)
            if enemy.pokemon.can_move():
                if enemy_move.use():
                    player.pokemon.take_damage(damage)
            show_message(f"{enemy.pokemon.name} attacks with {enemy_move.name}")
            if enemy_move.status_effect != "none":
                enemy_move.apply_effect(enemy.pokemon, player.pokemon)
                enemy.pokemon.apply_effect_damage(enemy.pokemon.status, player)
        return 1
    
    if player.pokemon.speed >= enemy.pokemon.speed:
        first = player
        second = enemy
        first_move = player_move
        second_move = enemy_move
    else:
        first = enemy
        second = player
        first_move = enemy_move
        second_move = player_move
    while (not(first.pokemon.is_fainted()) and not(second.pokemon.is_fainted())):
        first_move_damage = first_move.get_damage(first.pokemon,second.pokemon)
        if first.pokemon.can_move():
            if first_move.use():
                show_message(f"{first.pokemon.name} attacks with {first_move.name}")
                second.pokemon.take_damage(first_move_damage)
                
            else:
                continue
        if first_move.status_effect != "none":
            first_move.apply_effect(first.pokemon, second.pokemon)
            first.pokemon.apply_effect_damage(first.pokemon.status,second)
        t+=1
        if t==2:
            break
        first,second = second,first
        first_move,second_move = second_move,first_move
    if not(first.pokemon.is_fainted()) and not(second.pokemon.is_fainted()):
        return 1
    return 0


def choose_pokemon(player_pokemon, enemy_weights,party):
    best_poke_score = 0
    chosen_enemy = None
    for e_pokemon in party:
            if e_pokemon.hp > 0:
                poke_score = score_pokemon(e_pokemon, player_pokemon, enemy_weights)
                if poke_score > best_poke_score:
                    best_poke_score = poke_score
                    chosen_enemy = e_pokemon
    show_message(f"Challenger chose {chosen_enemy.name} - {chosen_enemy.level}")
    return chosen_enemy


