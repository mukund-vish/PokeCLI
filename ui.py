from constants import starters_id, items

categories = {
    1 : ["battle"],
    2 : ["encounter","explore"]
}


def show_message(message):
    print(message)
    
def get_player_name():
    name = input()
    return name

def starter_menu(data,info):
    for name in data:
        poke_id = data[name]["id"]
        show_message(f"{poke_id} - {data[name]["name"].title()}")
        info[poke_id] = data[name]["name"]
    while True:
        try:
            show_message("Enter the Id of your choice")
            selected_id = int(input())
            if selected_id not in starters_id:
                show_message("Not a valid Id for now.")
                continue
        except ValueError:
            show_message("Ids are number before the pokemon names")
            continue
        return selected_id
    


def showing_choices():
    show_message("What do you want to do:")
    show_message("1. Train\n2. Explore\n3. Shop\n4. Player Profile\n5. Inventory")
    while(True):
        try:
            show_message("Enter choice no. or press q to quit")
            choice =input()
            int_choice = int(choice)
            if int_choice not in [1,2,3,4,5]:
                show_message("Invalid Selection")
                continue
        except ValueError:
                if choice.lower() == 'q':
                    return choice.lower()
                else:
                    show_message("Give choice number please")
                    continue
        
        return int_choice


def main_menu():
    try:
        show_message("1. New Game\n2. Old Game")
        user_choice =  input()
        choice = int(user_choice)
        if choice not in [1,2]:
            return 0
        return choice
    except ValueError:
        show_message("Choices are given in Numbers")
        return 0
    
def encounter_method():
    try:
        show_message("What do you want to do ?")
        show_message("1. Throw a catch ball\n2. Throw a Rock\n3. Run")
        choice =  input("You[1 or 2 or 3] :")
        if choice not in ['1','2','3']:
            show_message("Invalid Selection")
            return 0
    except ValueError:
        show_message("Choices are in Numbers.")
        return 0
    return int(choice)

def get_user_in(message):
    show_message(message)
    option_in = input()
    if option_in.lower() not in ['yes','y']:
        return 0
    return option_in


def select_category():
    show_message("You want to shop for :")
    show_message("1. Battle, 2. Encounter")
    while True:
        try:
            category = int(input("1 or 2 :"))
            if category in (1, 2):
                return category
            show_message("Invalid selection. Please choose 1 or 2.")
        except ValueError:
            show_message("Please enter a valid number.")

def select_items(category):
    for item in items:
        item_info = items[item]
        if item_info["usable_in"] in categories[category] and item_info["price"]:
            show_message(f"{item_info["id"]} - {item.title()} - {item_info["price"]}")
    while True:
                try:
                    show_message("Select the id of the item to buy it.")
                    user_item=int(input("ID : "))
                    item_quantity = int(input("Quantity : "))
                    for item in items:
                        if items[item]["id"] == user_item:
                            return [item,item_quantity]
                except ValueError:
                    continue
                
def capsule_quantity():
    show_message("How much capsules you want to use")
    user_in = int(input())
    return user_in % 5

def ask_user_pokemon(player):
    show_message("Which Pokemon do you choose :")
    i=0
    for pokemon in player.party:
        i+=1
        print(f"{i}. {pokemon.name} - Level {pokemon.level} - EXPS {pokemon.exp}")
    show_message("Enter the coressponding number from name.")
    user_choice = int(input())
    return player.party[user_choice-1]

def get_user_move(pokemon):
    i = 0 
    for moves in pokemon.moves:
        i+=1
        print(f"{i}. {moves.name} - {moves.pp}")
    show_message("Select a number corressponding.")
    move = int(input())
    return pokemon.moves[move-1]


def get_battle_menu_choice():
    while True:
        show_message("What will you do?")
        show_message("1. Fight")
        show_message("2. Items")
        show_message("3. Switch")
        show_message("4. Run")
        show_message("Enter choice (1/2/3/4): ")
        choice = int(input("You [1 or 2 or 3 or 4]"))
        if choice in (1, 2, 3, 4):
            return choice
        show_message("Invalid choice, please select 1 or 2 or 3 or 4.")
        

def want_to_heal(player):
    show_message("Would you like heal all of your pokemons back to perfect health!")
    usr = get_user_in("For $20/each(Y/N)")
    if usr:
        total_amount = 20 * len(player.party)
        if player.spend_money(total_amount):
            show_message(f"Remaining balance {player.money}")
        else:
            show_message(f"Not enough Money to heal!")
        return 1
    return 0

def get_user_item(player,battle=True):
    while True:
        i = 0
        for p in player.items:
            i += 1
            show_message(f"{i}.{p} - {player.items[p]}")
        show_message("Enter the coressponding number from the name.")
        usr = input("You [number or q for exit]")
        if usr.lower() == 'q':
            return 0
        try:
            keys = list(player.items.keys())
            selected_item = keys[int(usr) - 1]
        except (ValueError, IndexError):
            show_message("Invalid selection. Please choose a valid item number.")
            continue
        if battle:
            if items[selected_item]["usable_in"] != "battle":
                show_message("You cannot use this item right now")
                continue
        else:
            if items[selected_item]["usable_in"] != "encounter" or items[selected_item]["usable_in"] in ["catch_balls","capsule"]:
                    show_message("You cannot use this item right now")
                    continue
        return selected_item


def get_user_pc(player):
    if not player.pc_storage:
        show_message("Your PC is empty.")
        return 0
    else:
            i = 0
            for name, (pokemon, count) in player.pc_storage.items():
                i += 1
                show_message(f"{i}. {name.title()} - Count: {count}")
            show_message("Enter the corresponding number from the name.")
            while True:
                usr = input("You [number or q for exit]: ")
                if usr.lower() == 'q':
                    return 0
                try:
                    keys = list(player.pc_storage.keys())
                    selected_pokemon = player.pc_storage[keys[int(usr) - 1]][0]
                    return selected_pokemon
                except (ValueError, IndexError):
                    show_message("Invalid selection. Please choose a valid number.")