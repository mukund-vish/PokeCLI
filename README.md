# PokéCLI 🎮

A **console-based Pokémon game** built entirely in Python — a prototype built to demonstrate solid grasp of core and intermediate Python concepts (OOP, data-driven design, JSON persistence, and game-state management) through a fully playable, text-driven RPG loop.

---

## 📖 About

**PokeCLI** is a turn-based, menu-driven Pokémon game that runs entirely in the terminal. You create a character, save your progress to disk, pick a starter, then train, explore, shop, and manage your party — all through simple numbered prompts.

Under the hood it's more than a menu loop: Pokémon have real stat formulas, growth curves, evolutions, and status effects; wild encounters are weighted by rarity and player level; trainer battles use a lightweight AI to pick moves and switch Pokémon; and everything is serialized to and from a JSON save file.

---

## ✨ Features

- **New Game / Load Game** — start fresh or resume from `saves/save.json`
- **Starter Selection** — choose from 27 starters spanning multiple generations
- **Turn-Based Trainer Battles** — Fight, use Items, Switch, or Run, against an AI-controlled challenger with its own party, move weighting, and level scaling
- **EXP & Leveling** — Pokémon and the player both level up on separate EXP curves, with growth rate (rookie / normal / veteran for the player, and rarity-based curves for Pokémon) affecting how fast that happens
- **Move Learning** — Pokémon learn new moves at specific levels, and you're prompted to swap out an old move if they already know 4
- **Evolution** — Pokémon evolve automatically once they hit their evolution level, with stats recalculated on the new form
- **Status Effects & Passive Abilities** — burns, poison, sleep, paralysis, confusion, freeze, leech seed, and passive flags like status immunity, always-first, ignore-type, and untouchable, all driven by data rather than hardcoded per-Pokémon
- **Exploration System** — random wild encounters, weighted by "bushes" (green / blue / red) that unlock rarer Pokémon as your player level increases
- **Catch Mechanic** — throw a Catch Ball, with rarity-based catch rates; charge it first using **Capsules** to boost your odds
- **Risk-Based Rock Throwing** — attempt to fight the wild Pokémon for item drops instead of catching it — succeed and it drops loot scaled to its rarity, fail and it costs you a life
- **Lives System** — 3 lives; hitting 0 wipes your save and restarts the game
- **Party & PC System** — active party is capped at 7; anything beyond that goes to your PC, and you can swap Pokémon between party and PC from your Player Profile
- **Shop & Items** — spend money on consumables and hold-item-style effects (stat buffs, HP healing, status cures, and riskier "gamble" items)
- **Player Profile** — view lives, badges, money, items, and full party status
- **Inventory** — view and select items to use in or out of battle
- **JSON Save System** — game state (player, party, PC, items, starter) is serialized to `saves/save.json` after nearly every action

---

## 🧠 Python Concepts Demonstrated

This project was built specifically to practice and showcase:

- **Object-Oriented Programming** — `Player`, `Pokemon`, `Move`, and battle-state classes (`BattleMon`, `BattleState`) encapsulating behavior and state
- **Data-driven design** — Pokémon, moves, and rarity tables live in JSON (`data/pokemon.json`, `data/moves.json`, `data/rarities.json`) rather than being hardcoded, so game content is decoupled from logic
- **File I/O & serialization** — `to_dict()` / `from_data()` patterns for converting live objects to/from JSON for save/load
- **Weighted randomness** — `random.choices()` used throughout for rarity tables, wild encounter bushes, trainer AI move/Pokémon selection, and catch/kill odds
- **Recursive-ish loop-based state machines** — leveling loops that handle multiple level-ups (and evolutions) from a single EXP gain in one pass
- **Modular program architecture** — logic is split across single-responsibility modules (`battle.py`, `battle_ai.py`, `encounter.py`, `leveling.py`, `money.py`, `shop.py`, `ui.py`, etc.) rather than one monolithic script
- **Dictionaries as flexible state containers** — status effects, temporary item effects, and passive flags are tracked as dicts with effect/value/duration tuples, ticked down each turn
- **Input validation & a console-driven UI layer** — all user I/O routed through a dedicated `ui.py` module, keeping game logic separate from `input()`/`print()` calls

---

## 🕹️ How to Play

### Requirements
- Python 3.x (standard library only — no external dependencies)

### Running the Game
```bash
git clone https://github.com/mukund-vish/PokeCLI.git
cd PokeCLI
python main.py
```

### Controls
The game is fully menu-driven — at every screen, type the number corresponding to your choice and press Enter, or `q` to quit at the main action menu (your progress is saved automatically before quitting).

---

## 📸 Sample Gameplay

```
Welcome to PokeCLI
1. New Game
2. Old Game
1
Please Enter Your Character's Name
leo
Game Saved!
Pick Any Pokemon of Your choice
1 - Bulbasaur
4 - Charmander
7 - Squirtle
...
Enter the Id of your choice
4
The charmander has joined your Party!
Game Saved!
What do you want to do:
1. Train
2. Explore
3. Shop
4. Player Profile
5. Inventory
Enter choice no. or press q to quit
```

**Training (Trainer Battle):**
```
Which Pokemon do you choose :
1. charmander - Level 5 - EXPS 1177
Enter the coressponding number from name.
1
Challenger chose mankey - 8
What will you do?
1. Fight
2. Items
3. Switch
4. Run
Enter choice (1/2/3/4):
```

**Exploring:**
```
azurill appeared.
What do you want to do ?
1. Throw a catch ball
2. Throw a Rock
3. Run
You[1 or 2 or 3] :
```

---

## 🗂️ Project Structure

```
PokeCLI/
├── main.py              # Entry point — main menu, save/load, game loop
├── ui.py                 # All console input/output (menus, prompts, messages)
├── player.py               # Player class — party, PC, lives, money, badges, EXP
├── pokemon.py                # Pokemon class — stats, leveling, evolution, status effects, items
├── starters.py                 # Starter selection menu & data
├── battle.py                    # Turn-based battle loop, BattleMon/BattleState
├── battle_ai.py                   # Opponent move & Pokémon selection logic
├── moves.py                        # Move class & data loading
├── move_selector.py                  # Selects movesets for wild/trainer Pokémon by level
├── encounter.py                        # Wild encounters, catching, rock-throwing, drops
├── leveling.py                           # EXP curves & level-up math for player & Pokémon
├── shop.py                                 # Shop categories & item purchasing
├── money.py                                  # Post-battle money calculation
├── constants.py                                # Shared config: growth rates, items, status effects
├── data/
│   ├── pokemon.json                              # Pokémon base stats, types, movesets, evolutions
│   ├── moves.json                                  # Move data (power, effects, etc.)
│   └── rarities.json                                 # Pokémon IDs grouped by rarity tier
├── saves/
│   └── save.json                                       # Generated at runtime — current save file
└── README.md
```

---

## 🙋 Why This Project?

This was built as a hands-on way to go beyond tutorial-level Python — designing a system with persistent state, multiple interacting components (battles, leveling, exploration, an item/effect system, saves), and real data-driven content, without relying on any external game framework.

---

## 📄 License

This project is open source. Add a [LICENSE](LICENSE) file (e.g. MIT) if you'd like to make the terms explicit.
