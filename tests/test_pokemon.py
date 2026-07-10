
import json
import pytest

from pokemon import Pokemon, all_pokemon


def make_pokemon(name="charmander", level=5, hp=None):
    data = all_pokemon[name]
    max_hp = ((2 * data["base_hp"] * level) // 100) + 10
    return Pokemon.from_data(
        data,
        current_hp=hp if hp is not None else max_hp,
        level=level,
        exps=0,
        moves=[],
    )


class TestStatCalculation:
    def test_max_hp_matches_formula(self):
        data = all_pokemon["charmander"]
        level = 12
        mon = make_pokemon("charmander", level=level)
        expected = ((2 * data["base_hp"] * level) // 100) + 10
        assert mon.max_hp == expected

    def test_attack_matches_formula(self):
        data = all_pokemon["charmander"]
        level = 12
        mon = make_pokemon("charmander", level=level)
        expected = ((2 * data["base_attack"] * level) // 100) + 5
        assert mon.attack == expected

    def test_higher_level_means_higher_stats(self):
        low = make_pokemon("charmander", level=5)
        high = make_pokemon("charmander", level=50)
        assert high.max_hp > low.max_hp
        assert high.attack > low.attack
        assert high.defense > low.defense
        assert high.speed > low.speed


class TestFaintingAndDamage:
    def test_is_fainted_false_above_zero_hp(self):
        mon = make_pokemon("charmander", level=5)
        assert mon.is_fainted() == 0

    def test_is_fainted_true_at_zero_hp(self):
        mon = make_pokemon("charmander", level=5, hp=0)
        assert mon.is_fainted() == 1

    def test_is_fainted_clamps_negative_hp_to_zero(self):
        mon = make_pokemon("charmander", level=5, hp=-10)
        assert mon.is_fainted() == 1
        assert mon.hp == 0

    def test_take_damage_reduces_hp(self):
        mon = make_pokemon("charmander", level=5)
        starting_hp = mon.hp
        mon.take_damage(5)
        assert mon.hp == starting_hp - 5

    def test_take_damage_returns_zero_and_faints_when_lethal(self):
        mon = make_pokemon("charmander", level=5)
        result = mon.take_damage(mon.hp + 100)
        assert result == 0
        assert mon.is_fainted() == 1

    def test_take_damage_returns_one_when_survives(self):
        mon = make_pokemon("charmander", level=5)
        result = mon.take_damage(1)
        assert result == 1


class TestLevelUp:
    def test_level_up_increments_level(self):
        mon = make_pokemon("charmander", level=5)
        mon.level_up()
        assert mon.level == 6

    def test_level_up_fully_heals_and_raises_max_hp(self):
        mon = make_pokemon("charmander", level=5)
        old_max_hp = mon.max_hp
        mon.level_up()
        assert mon.max_hp > old_max_hp
        assert mon.hp == mon.max_hp  # level up fully restores HP

    def test_level_up_recalculates_battle_stats(self):
        mon = make_pokemon("charmander", level=5)
        old_attack = mon.attack
        mon.level_up()
        assert mon.attack > old_attack


class TestEvolution:
    def test_charmander_evolves_at_level_16(self):
        # charmander -> charmeleon at level 16, per data/pokemon.json
        assert all_pokemon["charmander"]["evolves_at"] == 16
        assert all_pokemon["charmander"]["evolves_into"] == "charmeleon"

    def test_gain_exp_triggers_evolution_at_correct_level(self, monkeypatch):
        monkeypatch.setattr(Pokemon, "check_move", lambda self: None)

        mon = make_pokemon("charmander", level=15)
        assert mon.name == "charmander"
        
        for _ in range(50):
            if mon.level >= 16:
                break
            mon.gain_exp(mon.exp + 999999)  # force at least one level-up
            mon.exp = 0

        assert mon.level >= 16
        assert mon.name == "charmeleon"

    def test_evolve_does_nothing_if_no_evolution(self):
        mon = make_pokemon("venusaur", level=50)
        assert not all_pokemon["venusaur"]["evolves_into"]
        name_before = mon.name
        mon.evolve()
        assert mon.name == name_before


class TestSerialization:
    def test_to_dict_round_trip_preserves_core_fields(self):
        mon = make_pokemon("charmander", level=10)
        data = mon.to_dict()
        assert data["name"] == "charmander"
        assert data["level"] == 10
        assert data["hp"] == mon.hp
        assert data["rarity"] == mon.rarity

    def test_to_dict_is_json_serializable(self):
        mon = make_pokemon("charmander", level=10)
        # Should not raise — this is the exact operation used when saving.
        json.dumps(mon.to_dict())


class TestItemsAndEffects:
    def test_apply_item_hp_heals_without_exceeding_max(self):
        mon = make_pokemon("charmander", level=10, hp=1)
        mon.apply_item("healer", "hp", 0.5, None)
        assert mon.hp <= mon.max_hp
        assert mon.hp > 1

    def test_apply_item_stat_effect_scales_stat(self):
        mon = make_pokemon("charmander", level=10)
        original_attack = mon.attack
        mon.apply_item("attack-x", "attack", 1.5, 3)
        assert mon.attack == original_attack * 1.5
        assert "attack-x" in mon.items

    def test_tick_items_reverts_stat_after_duration_expires(self):
        mon = make_pokemon("charmander", level=10)
        original_attack = mon.attack
        mon.apply_item("attack-x", "attack", 1.5, 1)  # 1 turn duration
        mon.tick_items()  # turns: 1 -> 0, should revert and remove
        assert "attack-x" not in mon.items
        assert mon.attack == round((original_attack * 1.5) / 1.5)

    def test_apply_item_status_clears_status_conditions(self):
        mon = make_pokemon("charmander", level=10)
        mon.status = {"burn": 3, "poison": 2}
        mon.apply_item("full-heal", "status", None, None)
        assert mon.status == {}
