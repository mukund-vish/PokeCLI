from constants import items
from ui import show_message

def buy_item(player,item_info):
    item_price = items[item_info[0]]["price"]*item_info[1]
    if player.spend_money(item_price):
        player.add_item(item_info[0],item_info[1])
        show_message(f"{item_info[0]} has been added your inventory.")
        show_message(f"Your money remaining : {player.money}")
        return 1
    else:
        show_message(f"You cannot buy this particular item.\n Not enough Money!")
        return 0