import math
import pytest

from leveling import (
    pokemon_exps_to_level,
    pokemon_exps_to_next_level,
    player_exps_to_level,
    player_exps_to_next_level,
    level_gap_modifier,
    calculate_base_exp_yield,
    award_player,
    distribute_exps,
)

class TestPokemonExpsToLevel:
    def test_matches_formula_in_early_bracket(self):
        # level <= 20 -> floor(growth * 50 * level ** 1.8)
        level = 10
        growth = 1.0
        expected = math.floor(growth * 50 * level ** 1.8)
        assert pokemon_exps_to_level(level, growth) == expected

    def test_matches_formula_in_mid_bracket(self):
        # 20 < level <= 50 -> floor(growth * 80 * level ** 2.2)
        level = 30
        growth = 1.0
        expected = math.floor(growth * 80 * level ** 2.2)
        assert pokemon_exps_to_level(level, growth) == expected

    def test_matches_formula_in_high_bracket(self):
        # 50 < level <= 75 -> floor(growth * 120 * level ** 2.8)
        level = 60
        growth = 1.0
        expected = math.floor(growth * 120 * level ** 2.8)
        assert pokemon_exps_to_level(level, growth) == expected

    def test_matches_formula_past_75(self):
        # level > 75 -> floor(growth * 200 * level ** 2.8)
        level = 90
        growth = 1.0
        expected = math.floor(growth * 200 * level ** 2.8)
        assert pokemon_exps_to_level(level, growth) == expected

    def test_boundary_at_level_20_uses_early_formula(self):
        expected = math.floor(1.0 * 50 * 20 ** 1.8)
        assert pokemon_exps_to_level(20, 1.0) == expected

    def test_boundary_at_level_21_uses_mid_formula(self):
        expected = math.floor(1.0 * 80 * 21 ** 2.2)
        assert pokemon_exps_to_level(21, 1.0) == expected

    def test_rarity_growth_scales_requirement(self):
        # Higher rarity growth multiplier should require strictly more EXP
        # at the same level.
        common_growth = 0.7
        legendary_growth = 1.8
        common_req = pokemon_exps_to_level(10, common_growth)
        legendary_req = pokemon_exps_to_level(10, legendary_growth)
        assert legendary_req > common_req

    def test_requirement_increases_with_level(self):
        levels = [1, 5, 10, 20, 21, 30, 50, 51, 75, 76, 100]
        requirements = [pokemon_exps_to_level(lvl, 1.0) for lvl in levels]
        assert requirements == sorted(requirements)



class TestPokemonExpsToNextLevel:
    def test_is_difference_between_consecutive_levels(self):
        level = 15
        growth = 1.0
        expected = pokemon_exps_to_level(level + 1, growth) - pokemon_exps_to_level(level, growth)
        assert pokemon_exps_to_next_level(level, growth) == expected

    def test_is_never_negative(self):
        for level in [1, 19, 20, 21, 49, 50, 51, 74, 75, 76]:
            assert pokemon_exps_to_next_level(level, 1.0) >= 0

class TestPlayerExpsToLevel:
    def test_matches_formula_in_early_bracket(self):
        level = 5
        growth = 1.0
        expected = math.floor(growth * 200 * level ** 1.5)
        assert player_exps_to_level(level, growth) == expected

    def test_matches_formula_in_mid_bracket(self):
        level = 20
        growth = 1.0
        expected = math.floor(growth * 500 * level ** 2.0)
        assert player_exps_to_level(level, growth) == expected

    def test_matches_formula_in_high_bracket(self):
        level = 45
        growth = 1.0
        expected = math.floor(growth * 1000 * level ** 2.5)
        assert player_exps_to_level(level, growth) == expected

    def test_matches_formula_past_60(self):
        level = 65
        growth = 1.0
        expected = math.floor(growth * 2000 * level ** 3.0)
        assert player_exps_to_level(level, growth) == expected

    def test_rookie_requires_more_exp_than_veteran(self):
        rookie_req = player_exps_to_level(5, 1.2)
        veteran_req = player_exps_to_level(5, 0.8)
        assert rookie_req > veteran_req

    def test_next_level_never_negative(self):
        for level in [1, 9, 10, 11, 29, 30, 31, 59, 60, 61]:
            assert player_exps_to_next_level(level, 1.0) >= 0


class TestLevelGapModifier:
    @pytest.mark.parametrize(
        "attacker_level,defender_level,expected",
        [
            (10, 20, 1.5),   # gap == 10 
            (10, 25, 1.5),   # gap > 10 
            (10, 15, 1.2),   # gap == 5 
            (10, 17, 1.2),   # gap == 7
            (10, 10, 1.0),   # even level -> no modifier
            (10, 5, 1.0),    # gap == -5, within [-5, 5) -> no modifier
            (10, 4, 0.7),    # gap == -6 -> penalty starts
            (10, 1, 0.7),    # gap == -9, within [-10, -5)
            (20, 5, 0.4),    # gap == -15 -> harshest penalty
        ],
    )
    def test_gap_brackets(self, attacker_level, defender_level, expected):
        assert level_gap_modifier(attacker_level, defender_level) == expected

class FakePokemon:
    def __init__(self, level, rarity, fainted=False):
        self.level = level
        self.rarity = rarity
        self._fainted = fainted
        self.exp_gained = None

    def is_fainted(self):
        return self._fainted

    def gain_exp(self, amount):
        self.exp_gained = amount


class FakeBattleMon:
    def __init__(self, pokemon):
        self.pokemon = pokemon


class TestCalculateBaseExpYield:
    def test_matches_formula_same_level(self):
        attacker = FakePokemon(level=10, rarity="common")
        defeated = FakePokemon(level=10, rarity="common")
        base = 40  # base_exp_yield["common"]
        raw = math.floor(base * (defeated.level / 5))
        modifier = level_gap_modifier(attacker.level, defeated.level)  # == 1.0
        expected = math.floor(raw * modifier)
        assert calculate_base_exp_yield(defeated, attacker) == expected

    def test_higher_rarity_yields_more_exp(self):
        attacker = FakePokemon(level=10, rarity="common")
        common_defeated = FakePokemon(level=10, rarity="common")
        legendary_defeated = FakePokemon(level=10, rarity="legendary")
        common_yield = calculate_base_exp_yield(common_defeated, attacker)
        legendary_yield = calculate_base_exp_yield(legendary_defeated, attacker)
        assert legendary_yield > common_yield

    def test_unwraps_battlemon_via_pokemon_attribute(self):
        attacker = FakePokemon(level=10, rarity="common")
        defeated = FakePokemon(level=10, rarity="common")
        wrapped = FakeBattleMon(defeated)
        assert calculate_base_exp_yield(wrapped, attacker) == calculate_base_exp_yield(defeated, attacker)


class TestAwardPlayer:
    def test_scales_with_player_level(self):
        class FakePlayer:
            def __init__(self, level):
                self.level = level

        low_level = award_player(FakePlayer(level=1), "win_trainer_battle")
        high_level = award_player(FakePlayer(level=20), "win_trainer_battle")
        assert high_level > low_level

    def test_matches_formula(self):
        class FakePlayer:
            level = 5

        amount = 200  
        expected = math.floor(amount * (1 + 5 * 0.05))
        assert award_player(FakePlayer(), "win_trainer_battle") == expected


class TestDistributeExps:
    def test_fainted_pokemon_get_no_exp(self):
        fainted = FakeBattleMon(FakePokemon(level=10, rarity="common", fainted=True))
        alive = FakeBattleMon(FakePokemon(level=10, rarity="common", fainted=False))
        defeated = FakePokemon(level=10, rarity="common")

        distribute_exps([fainted, alive], defeated)

        assert fainted.pokemon.exp_gained is None
        assert alive.pokemon.exp_gained is not None

    def test_returns_zero_when_no_eligible_pokemon(self):
        fainted = FakeBattleMon(FakePokemon(level=10, rarity="common", fainted=True))
        defeated = FakePokemon(level=10, rarity="common")
        result = distribute_exps([fainted], defeated)
        assert result == 0

    def test_exp_is_split_between_multiple_survivors(self):
        solo = FakeBattleMon(FakePokemon(level=10, rarity="common"))
        distribute_exps([solo], FakePokemon(level=10, rarity="common"))
        solo_exp = solo.pokemon.exp_gained

        first = FakeBattleMon(FakePokemon(level=10, rarity="common"))
        second = FakeBattleMon(FakePokemon(level=10, rarity="common"))
        distribute_exps([first, second], FakePokemon(level=10, rarity="common"))

        assert first.pokemon.exp_gained < solo_exp
        assert second.pokemon.exp_gained < solo_exp
