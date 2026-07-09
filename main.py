from player import Player
from pokemon import Pokemon
from starters import selected_pokemon, starter_list
from encounter import wild_encounter,start_encounter,get_trainer_pokemon
from shop import buy_item
from moves import Move
from ui import *
from battle import *
from battle_ai import run_move, choose_pokemon
from leveling import distribute_exps,player_level_up
from money import calculate_money
import json
import os
import shutil
import random
from constants import score_move_weight,score_pokemon_weights,items

def new_player():
    show_message("Please Enter Your Character's Name")
    name = get_player_name()
    player = Player(name)
    player.player_type()
    save_game(player)
    return player


def save_game(player):
    os.makedirs("saves", exist_ok=True)
    with open("saves/save.json", "w") as f:
        json.dump(player.to_dict(), f, indent=4)
    show_message("Game Saved!")

def load_game():
    if not os.path.exists("saves/save.json"):
        show_message("No save file found!")
        return None
    
    with open("saves/save.json") as f:
        data = json.load(f)
    
    player = Player(data["name"])
    player.lives = data["lives"]
    player.money = data["money"]
    player.level = data["level"]
    player.badges = data["badges"]
    player.items = data["items"]
    player.exp = data["exp"]
    player.growth = data["growth"] or player.player_type()
    player.starter = Pokemon.from_data(data["starter"], data["starter"]['hp'], data["starter"]["level"], data["starter"]['exp'], [(Move.from_data(moves)) for moves in data["starter"]["moves"]]) if data["starter"] else None
    
    for poke_data in data["party"]:
        pokemon = Pokemon.from_data(poke_data, poke_data['hp'],poke_data["level"],poke_data['exp'], [(Move.from_data(moves)) for moves in poke_data["moves"]])
        player.party.append(pokemon)
    
    if data["pc_storage"]:
        for poke_name, (poke_data, count) in data["pc_storage"].items():
            pc = Pokemon.from_data(poke_data, poke_data['hp'],poke_data["level"],poke_data['exp'], [(Move.from_data(moves)) for moves in poke_data["moves"]])
            player.pc_storage[pc.name] = [pc, count]
    else:
        player.pc_storage = {}
    
    return player

def select_starter(player):
    info = {}
    show_message("Pick Any Pokemon of Your choice")
    data = starter_list()
    selected_id = starter_menu(data,info)
    starter = selected_pokemon(data[info[selected_id]])
    add_to_party(player,starter)
    player.starter = starter
    return starter

def add_to_party(player,pokemon):
    player.add_pokemon(pokemon)

def starter_pack(player):
    pack={
        "catch_balls":5,
        "capsule":5
    }
    player.add_items(pack)
    player.money = 500


def which_bush(player_level):
    if player_level >=50:
        bushes = ["green","blue","red"]
        weights = [35,50,15]
    elif player_level >=20:
        bushes = ["green","blue"]
        weights = [50, 50]
    elif player_level <=10:
        bushes = ["green"]
        weights = [100]
    
    return random.choices(bushes,weights=weights,k=1)[0]

def explore(player):
    player.remove_item()
    bush = which_bush(player.level)
    poke_wild = wild_encounter(player.level,bush,player.items_using,player.items)
    show_message(f"{poke_wild.name} appeared.")
    result = start_encounter(player,poke_wild,player.items,player.items_using)
    if result:
            if not add_to_party(player,poke_wild):
                show_message("The Pokémon has been sent to your PC.")
                player.pc_storage[poke_wild.name] = [poke_wild, player.pc_storage.get(poke_wild.name, 0) + 1]
                return 1
    else:
        return 0
    
def shop(player):
    category = select_category()
    item_info = select_items(category)
    buy_item(player,item_info)
    
def setup_trainer(player):
    lvl_sum = sum(p.level for p in player.party)
    max_lvl = max((p.level for p in player.party), default=1)
    avg_lvl = lvl_sum // len(player.party) if player.party else 1
    trainer_level = random.randint(
        avg_lvl - 5 if avg_lvl > 5 else avg_lvl,
        avg_lvl + 5
    )
    party_capacity = random.randint(1, 7)
    enemy_party = [get_trainer_pokemon(max_lvl, trainer_level+1) for _ in range(party_capacity)]
    return trainer_level, party_capacity, enemy_party


def setup_enemy_type():
    enemy_type = random.choice([p_type for p_type in score_pokemon_weights])
    enemy_weights = score_pokemon_weights[enemy_type]
    enemy_move_weights = score_move_weight[enemy_type]
    return enemy_weights, enemy_move_weights


def select_player_pokemon(player):
    while True:
        player_pokemon = BattleMon(ask_user_pokemon(player), len(player.party))
        if player_pokemon.pokemon.hp > 0:
            return player_pokemon
        show_message("This Pokémon is already fainted.")


def handle_fight(current_state, player_pokemon, chosen_enemy, enemy_move_weights):
    player_move = get_user_move(player_pokemon.pokemon)
    run_move(player_move, current_state, enemy_move_weights)
    show_message(f"{chosen_enemy.name}'s remaining HP: {chosen_enemy.hp}")
    show_message(f"{player_pokemon.pokemon.name}'s remaining HP: {player_pokemon.pokemon.hp}")


def use_item(item, target, opponent=None):
    item_data = items[item]
    name     = item_data["name"]
    effect   = item_data["effect"]
    value    = item_data["value"]
    turns    = item_data["turns"]

    if name in target.items:
        show_message("This item is already in effect!")
        return 0

    target.apply_item(name, effect, value, turns, opponent)
    show_message(f"{target.name} used {name}!")
    return 1


def handle_items(player, current_state):
    user_item = get_user_item(player)
    if not user_item:
        return

    item_data = items[user_item]
    if item_data["usable_in"] != "battle":
        show_message("Can't use that item in battle!")
        return

    target_poke = ask_user_pokemon(player)
    opponent = current_state.enemy.pokemon

    result = use_item(user_item, target_poke, opponent)
    if result:
        player.items[user_item] -= 1
        if player.items[user_item] <= 0:
            del player.items[user_item]
            

def handle_switch(player):
    show_message("Select a Pokémon to switch in:")
    new_pokemon = ask_user_pokemon(player)
    if new_pokemon.hp <= 0:
        show_message("Can't switch to a fainted Pokémon!")
        return None
    show_message(f"Switching to {new_pokemon.name}!")
    return new_pokemon
def run_turn(player, current_state, player_pokemon, chosen_enemy, enemy_move_weights):
    choice = get_battle_menu_choice()

    if choice == 1:
        player_move = get_user_move(player_pokemon.pokemon)
        run_move(player_move, current_state, enemy_move_weights)
    elif choice == 2:
        handle_items(player, current_state)
        run_move(None, current_state, enemy_move_weights)
    elif choice == 3:
        new_pokemon = handle_switch(player)
        if new_pokemon:
            player_pokemon = BattleMon(new_pokemon, len(player.party))
            current_state.player = player_pokemon
        run_move(None, current_state, enemy_move_weights)
    elif choice == 4:
        if random.random() < 0.5:
            show_message("You ran away safely!")
            return player_pokemon
        show_message("You failed to run away!")
        run_move(None, current_state, enemy_move_weights)

    show_message(f"{chosen_enemy.name}'s remaining HP: {chosen_enemy.hp}")
    show_message(f"{player_pokemon.pokemon.name}'s remaining HP: {player_pokemon.pokemon.hp}")
    player_pokemon.pokemon.tick_items()
    chosen_enemy.tick_items()
    return player_pokemon  

def handle_enemy_fainted(player_pokemon, chosen_enemy, enemy_party,
                          enemy_weights, party_capacity,
                          used_pokemons, enemy_alive):
    enemy_alive -= 1
    distribute_exps(used_pokemons, chosen_enemy)
    used_pokemons.clear()

    if enemy_alive <= 0:
        return None, enemy_alive, False

    usr = get_user_in("Do you want to continue (y/n)")
    if not usr:
        return None, enemy_alive, False

    chosen_enemy = choose_pokemon(player_pokemon, enemy_weights, enemy_party)
    return chosen_enemy, enemy_alive, True

def resolve_battle(player, enemy_party, turns, player_alive):
    if player_alive > 0:
        winner = player.name
        player_level_up(player, "win_trainer_battle")
        money = calculate_money(player, enemy_party, turns)
        player.earn_money(money)
    else:
        winner = "Challenger"

    show_message(f"{winner} won.")


def battle(player):
    if not player.is_able_to_battle():
        show_message("All of your pokemons are fainted!")
        usr = want_to_heal(player)
        if usr:
            for p in player.party:
                p.hp = p.max_hp
            show_message("Your party is back to perfect health!")
        return
    turns = 0
    used_pokemons = []

    _, party_capacity, enemy_party = setup_trainer(player)
    enemy_weights, enemy_move_weights = setup_enemy_type()

    player_alive = sum(1 for p in player.party if p.hp > 0)
    enemy_alive = party_capacity
    choose_enemy = True

    while player_alive > 0 and enemy_alive > 0:
        player_pokemon = select_player_pokemon(player)

        if choose_enemy:
            chosen_enemy = choose_pokemon(player_pokemon, enemy_weights, enemy_party)

        if player_pokemon not in used_pokemons:
            used_pokemons.append(player_pokemon)

        if chosen_enemy is None:
            break

        current_state = BattleState(player_pokemon, BattleMon(chosen_enemy, party_capacity))
        choose_enemy = False

        while player_alive > 0 and enemy_alive > 0:
            player_pokemon=run_turn(player,current_state, player_pokemon, chosen_enemy, enemy_move_weights)
            turns += 1

            if chosen_enemy.is_fainted():
                chosen_enemy, enemy_alive, should_continue = handle_enemy_fainted(player_pokemon, chosen_enemy, enemy_party,                                                                                 enemy_weights, party_capacity,
                                                                                 used_pokemons, enemy_alive)
                if not should_continue:
                    break
                if player_pokemon not in used_pokemons:
                    used_pokemons.append(player_pokemon)
                current_state = BattleState(player_pokemon, BattleMon(chosen_enemy, party_capacity))
                continue

            if player_pokemon.pokemon.is_fainted():
                player_alive = sum(1 for p in player.party if p.hp > 0)
                if player_alive == 0:
                    break
                break

    resolve_battle(player, enemy_party, turns, player_alive)


def inventory(player):
    for item, quantity in player.items.items():
        show_message(f"{item}: {quantity}")
        usr_item = get_user_item(player,False)
        if usr_item:
            player.items_using ={
                "item":usr_item,
                "turns":items[usr_item]["turns"],
                "effect":items[usr_item]["effect"],
                "value":items[usr_item]["value"]
            }
        else:
            return
def main():
        show_message("Welcome to PokeCLI")
        while True:
            choice = main_menu()
            
            if choice:
                if choice == 1:
                    player = new_player()
                    select_starter(player)
                    starter_pack(player)
                    break
                elif choice == 2:
                    player = load_game()
                    if not(player):
                        show_message("No saved game Found. Starting a New Game....")
                        player = new_player()
                        select_starter(player)
                        starter_pack(player)
                        break
                    else:
                        show_message(f"{player.name} welcome back.")
                        break
            else:
                continue
        while True:
            save_game(player)
            if player.lives:
                play_choice = showing_choices()
                
                if play_choice == 1: #train
                    battle(player)
                
                elif play_choice == 2: #explore
                    explore(player)
                elif play_choice == 3: #shop
                    shop(player)
                elif play_choice == 4: #player profile
                    player.show_status()
                elif play_choice == 5: # inventory
                    inventory(player)
                elif play_choice == 'q':
                    show_message("ThankYou for Playing.")
                    show_message("Saving your Data....")
                    save_game(player)
                    break
            else:
                shutil.rmtree("saves/")
                main()
main()

