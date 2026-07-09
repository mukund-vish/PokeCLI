from ui import show_message, get_user_in, get_user_pc, ask_user_pokemon
from leveling import player_exps_to_level
from constants import player_growth
class Player:
    def __init__(self,name):
        self.name=name.title()
        self.lives=3
        self.money=0
        self.level=1
        self.badges=[]
        self.party=[]
        self.items={}
        self.items_using = {}
        self.exp=0
        self.growth=None
        self.pc_storage={}
        self.starter = None
    def to_dict(self):
        return {
            "name": self.name,
            "lives": self.lives,
            "money": self.money,
            "level": self.level,
            "badges": self.badges,
            "party": [p.to_dict() for p in self.party],
            "items": self.items,
            "items_using": self.items_using,
            "exp" : self.exp,
            "growth" : self.growth,
            "pc_storage" : {name: [poke.to_dict(), count] for name, (poke, count) in self.pc_storage.items()},
            "starter" : self.starter.to_dict() if self.starter else None
        }
        
    def player_type(self):
        if self.level <=10:
            self.growth = "rookie"
        elif self.level <=30:
            self.growth = "normal"
        else:
            self.growth = "veteran"
    def add_pokemon(self,pokemon):
        if len(self.party)>=7:
            show_message("Your Party is Full!")
            return 0
        self.party.append(pokemon)
        show_message(f"The {pokemon.name} has joined your Party!")
        return 1
    def add_item(self,item_name,quantity):
        self.items[item_name] = quantity
    
    def add_items(self,items):
        for item, quantity in items.items():
            self.items[item] = self.items.get(item, 0) + quantity
    
    def remove_item(self):
        if self.items:
            for p in self.items:
                if self.items[p]<=0:
                        del self.items[p]
                        return 1
    def lose_life(self):
        self.lives-=1
        show_message(f"Your have lost your life. {self.lives} Remaining.")
        if self.lives==0:
            show_message("Game Over ! Resetting....")
            return 0
        return 1
    
    def earn_money(self, amount):
        self.money+=amount
        show_message(f"You earned ${amount}! Total : ${self.money}")
        return 1

    def spend_money(self,amount):
        if amount>self.money:
            return 0
        self.money-=amount
        if self.money<=0:
            self.money=0
        return 1
    
    def add_badges(self, badge):
        self.badges.append(badge)
        show_message(f"{badge} added to your inventory.")
        return 1
    
    def show_party(self):
        show_message(f"\n{self.name}'s Party")
        if self.party:
            for i,pokemon in enumerate(self.party, 1):
                show_message(f"{i}. {pokemon.name.title()} — HP : {pokemon.hp} / {pokemon.max_hp}")
            return 1
        show_message(f"Nothing to see here.")
        return 0
    
    def gain_exp(self, amount):
        self.exp += amount
        show_message(f"{self.name} gained {amount} XP!")
        while True:
            exps_next = player_exps_to_level(self.level, player_growth[self.growth])
            if self.exp >= exps_next:
                self.exp -= exps_next
                self.level+=1
            else:
                break
    
    def show_status(self):
        show_message(f"\n--- {self.name}'s Status ---")
        show_message(f"Lives: {self.lives}/3")
        show_message(f"Badges: {len(self.badges)}")
        show_message(f"Money: ${self.money}")
        show_message(f"Items: {self.items if self.items else 'None'}")
        self.show_party()
        usr = get_user_in("Do you want to check your PC? (Y/N)")
        if usr:
            poke = get_user_pc(self)
            if poke:
                show_message(f"Which pokemon you want to switch ?")
                switch = ask_user_pokemon(self)
                if switch:
                    self.party.remove(switch)
                    self.pc_storage[switch.name] = [switch, self.pc_storage.get(switch.name, 0) + 1]
                    self.add_pokemon(poke)
                    show_message(f"{switch.name} has been sent to PC.")
        else:
            return
    
    def is_able_to_battle(self):
        i=0
        for p in self.party:
            if p.hp<=0:
                i+=1
        if i == len(self.party):
            return 0
        return 1