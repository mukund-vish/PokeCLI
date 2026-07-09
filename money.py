def give_money(player,enemy_highest_level, faint_count, turns,expected_turns):
    base = enemy_highest_level*5
    avg_hp = sum(p.hp for p in player.party) / len(player.party)
    max_avg_hp = sum(p.max_hp for p in player.party) / len(player.party)
    hp_percent = (avg_hp / max_avg_hp) * 100
    
    multiplier = 1.0
    
    if hp_percent > 75:
        multiplier = 1.5
    elif hp_percent > 50:
        multiplier = 1.25
    elif hp_percent > 25:
        multiplier = 1.0
    else:
        multiplier = 0.85
    
    multiplier -= faint_count*0.10
    if turns > expected_turns:
        multiplier -=0.10
        
    multiplier = max(multiplier, 0.1)
    reward = round(base * multiplier)
    return reward

def calculate_money(player,enemy_party, turns):
    enemy_highest_lvl = 0
    for e_p in enemy_party:
        if e_p.level > enemy_highest_lvl:
            enemy_highest_lvl = e_p.level
    
    faint_count=0
    for p_p in player.party:
        if p_p.hp<=0:
            faint_count+=1
    
    expected_turns = len(enemy_party)*3+5
    money_gained = give_money(player,enemy_highest_lvl,faint_count,turns,expected_turns)
    return money_gained
        