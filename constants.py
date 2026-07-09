type_chart = {
    "normal":   {"rock": 0.5, "ghost": 0, "steel": 0.5},
    "fire":     {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2},
    "water":    {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5},
    "electric": {"water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5},
    "grass":    {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5},
    "ice":      {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5},
    "fighting": {"normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5},
    "poison":   {"grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0, "fairy": 2},
    "ground":   {"fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2},
    "flying":   {"electric": 0.5, "grass": 2, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5},
    "psychic":  {"fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5},
    "bug":      {"fire": 0.5, "grass": 2, "fighting": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5, "dark": 2, "steel": 0.5, "fairy": 0.5},
    "rock":     {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5},
    "ghost":    {"normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5},
    "dragon":   {"dragon": 2, "steel": 0.5, "fairy": 0},
    "dark":     {"fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "fairy": 0.5},
    "steel":    {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5, "fairy": 2},
    "fairy":    {"fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2, "dark": 2, "steel": 0.5},
}

non_movement = {
    "freeze": 20,
    "sleep": 0,
    "paralysis": 25,
    "confusion": 33,
    "flinch": 0
}

status_damage = {
    "burn": 1/16,      
    "poison": 1/8,      
    "bad-poison": 1/16, 
    "curse": 1/4,       
    "nightmare": 1/4,   
    "leech-seed": 1/8,  
}

starters_id = [1, 4, 7, 152, 155, 158, 252, 255, 258, 387, 390, 393, 495, 498, 501, 650, 653, 656, 722, 725, 728, 810, 813, 816, 906, 909, 912]

items = {
    "healer": {
        "id": 1,
        "name": "Healer",
        "description": "Restores 50% of your Pokemon's HP instantly.",
        "effect": "hp",
        "value": 0.5,
        "turns": None,
        "usable_in": "battle",
        "price": 200
    },
    "attack-x": {
        "id": 2,
        "name": "Attack X",
        "description": "Boosts your Pokemon's attack by 1.5x for 3 turns.",
        "effect": "attack",
        "value": 1.5,
        "turns": 3,
        "usable_in": "battle",
        "price": 350
    },
    "defense-x": {
        "id": 3,
        "name": "Defense X",
        "description": "Boosts your Pokemon's defense by 1.5x for 3 turns.",
        "effect": "defense",
        "value": 1.5,
        "turns": 3,
        "usable_in": "battle",
        "price": 350
    },
    "speed-x": {
        "id": 4,
        "name": "Speed X",
        "description": "Boosts your Pokemon's speed by 1.5x for 3 turns.",
        "effect": "speed",
        "value": 1.5,
        "turns": 3,
        "usable_in": "battle",
        "price": 350
    },
    "accuracy-x": {
        "id": 5,
        "name": "Accuracy X",
        "description": "Boosts your Pokemon's accuracy by 1.5x for 3 turns.",
        "effect": "accuracy",
        "value": 1.5,
        "turns": 3,
        "usable_in": "battle",
        "price": 350
    },
    "gainer": {
        "id": 6,
        "name": "Gainer",
        "description": "Doubles XP gained from the next battle.",
        "effect": "xp",
        "value": 2.0,
        "turns": 1,
        "usable_in": "battle",
        "price": 500
    },
    "status-heal": {
        "id": 7,
        "name": "Status Heal",
        "description": "Instantly removes all status effects from your Pokemon.",
        "effect": "status",
        "value": None,
        "turns": None,
        "usable_in": "battle",
        "price": 300
    },
    "capsule": {
        "id": 8,
        "name": "Capsule",
        "description": "Charges your Catch Ball, increasing catch rate by 10%.",
        "effect": "catch-rate",
        "value": 10,
        "turns": None,
        "usable_in": "encounter",
        "price": 1500
    },
    "flee-freeze": {
        "id": 9,
        "name": "Flee Freeze",
        "description": "Freezes the wild Pokemon's flee timer for 5 turns.",
        "effect": "flee-timer",
        "value": 5,
        "turns": None,
        "usable_in": "encounter",
        "price": 600
    },
    "lure-stone": {
        "id": 10,
        "name": "Lure Stone",
        "description": "Guarantees a rare wild Pokemon encounter on your next bush visit.",
        "effect": "encounter-rate",
        "value": 100,
        "turns": None,
        "usable_in": "explore",
        "price": 400
    },
    "rarity-charm": {
        "id": 11,
        "name": "Rarity Charm",
        "description": "Bumps up the rarity of the next wild Pokemon encounter by one tier.",
        "effect": "rarity",
        "value": 1,
        "turns": None,
        "usable_in": "explore",
        "price": 800
    },
    "rage-fuel": {
        "id": 12,
        "name": "Rage Fuel",
        "description": "When HP drops below 20%, attack doubles for 2 turns.",
        "effect": "attack",
        "value": 2.0,
        "turns": 2,
        "trigger": "low-hp",
        "usable_in": "battle",
        "price": 0
    },
    "mirror-dust": {
        "id": 13,
        "name": "Mirror Dust",
        "description": "Reflects the next status effect back at the opponent.",
        "effect": "reflect-status",
        "value": None,
        "turns": 1,
        "usable_in": "battle",
        "price": 0
    },
    "null-stone": {
        "id": 14,
        "name": "Null Stone",
        "description": "Makes your Pokemon completely immune to status effects for 3 turns.",
        "effect": "status-immunity",
        "value": None,
        "turns": 3,
        "usable_in": "battle",
        "price": 0  
    },
    "chaos-shard": {
        "id": 15,
        "name": "Chaos Shard",
        "description": "Hurls a random status effect at the opponent. Could be anything!",
        "effect": "random-status",
        "value": None,
        "turns": None,
        "usable_in": "battle",
        "price": 0
    },
    "type-breaker": {
        "id": 16,
        "name": "Type Breaker",
        "description": "Your next move ignores type effectiveness completely.",
        "effect": "ignore-type",
        "value": None,
        "turns": 1,
        "usable_in": "battle",
        "price": 0
    },
    "speed-surge": {
        "id": 17,
        "name": "Speed Surge",
        "description": "Your Pokemon always moves first for 3 turns regardless of speed.",
        "effect": "always-first",
        "value": None,
        "turns": 3,
        "usable_in": "battle",
        "price": 0
    },
    "ghost-veil": {
        "id": 18,
        "name": "Ghost Veil",
        "description": "Your next 2 moves cannot miss no matter what.",
        "effect": "no-miss",
        "value": None,
        "turns": 2,
        "usable_in": "battle",
        "price": 0
    },
    "power-drain": {
        "id": 19,
        "name": "Power Drain",
        "description": "Steals 30% of opponent's attack stat and adds it to yours.",
        "effect": "steal-attack",
        "value": 0.3,
        "turns": None,
        "usable_in": "battle",
        "price": 0
    },
    "berserker-chip": {
        "id": 20,
        "name": "Berserker Chip",
        "description": "Doubles attack for 3 turns but disables all status moves.",
        "effect": "berserker",
        "value": 2.0,
        "turns": 3,
        "usable_in": "battle",
        "price": 0
    },
    "last-stand": {
        "id": 21,
        "name": "Last Stand",
        "description": "At 1 HP, your next move deals 3x damage.",
        "effect": "last-stand",
        "value": 3.0,
        "turns": 1,
        "trigger": "1hp",
        "usable_in": "battle",
        "price": 0
    },
    "soul-gamble": {
        "id": 22,
        "name": "Soul Gamble",
        "description": "50% chance to fully heal your Pokemon. 50% chance to instantly faint it.",
        "effect": "gamble",
        "value": None,
        "turns": None,
        "usable_in": "battle",
        "price": 0
    },
    "legendary-aura": {
        "id": 23,
        "name": "Legendary Aura",
        "description": "Dropped only by Legendaries. Makes your Pokemon completely untouchable for 1 turn.",
        "effect": "untouchable",
        "value": None,
        "turns": 1,
        "usable_in": "battle",
        "price": 0
    },
    "catch_balls":{
        "id": 24,
        "name": "catch_balls",
        "description":"Tool used for catching wild Pokemons.",
        "effect":"none",
        "turns":"none",
        "usable_in":"explore",
        "price":200
    }
}


score_move_weight={
    "aggressive" :{"damage": 1.0, "accuracy": 0.2, "status": 0.1},
    "balanced"   : {"damage": 0.6, "accuracy": 0.6, "status": 0.5},
    "defensive"  : {"damage": 0.2, "accuracy": 0.9, "status": 1.2},
    "status"     : {"damage": 0.2, "accuracy": 0.7, "status": 2.0}
}


score_pokemon_weights = {
    "aggressive" : {"effectiveness": 1.0, "hp": 0.2, "coverage": 0.6},
    "balanced"   : {"effectiveness": 0.6, "hp": 0.6, "coverage": 0.5},
    "defensive"  : {"effectiveness": 1.0, "hp": 2.0, "coverage": 0.2},
    "status"     : {"effectiveness": 0.2, "hp": 2.0, "coverage": 0.7},
}


pokemon_growth = {
    "common":      0.7,
    "uncommon":    1.0,
    "rare":      1.3,
    "mythical" : 1.5,
    "legendary": 1.8,
}


player_growth = {
    "veteran":    0.8,
    "normal":     1.0,
    "rookie":     1.2,
}

base_exp_yield = {
    "common":    40,
    "uncommon":  70,
    "rare":      120,
    "mythical":  180,
    "legendary": 250
}

player_exp_sources = {
    "win_trainer_battle":   200,
    "win_gym_battle":       500,
    "catch_pokemon":        80,
    "catch_new_rarity":    150,   
    "evolve_pokemon":       120,
    "catch_legendary":       300,
    "new_item" : 100,
}