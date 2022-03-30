"""
Test file
"""
import re
from pathlib import Path
from unittest import TestCase
from models.round import PlayerKill, PlayerAttack,DamageState

from .get_match_data import get_game_object, MatchRegex, get_game_data


class TestRegex(TestCase):
    """
    Test suit for the regular expressions
    and parsers
    """
    def test_get_rounds(self):
        """
        Check if you get the right number of rounds
        based on the test data
        """
        test_data_path = Path('./src/assets/data.txt')
        results = get_game_data(test_data_path)
        self.assertEqual(len(results), 22)

    def test_game_start(self):
        """
        Test capturing the match start
        """
        entry_true = "11/28/2021 - 20:41:09:  [FACEIT^] LIVE!"
        result = re.match(MatchRegex.FACE_IT_LIVE.value, entry_true)

        self.assertTrue(result)

        entry_false = "1wefwefwef"
        result = re.match(MatchRegex.FACE_IT_LIVE.value, entry_false)

        self.assertEqual(result, None)

    def test_get_attack_action(self):
        """
        Test parsing of the attack entry
        """
        # pylint: disable=line-too-long
        entry_value = '11/28/2021 - 20:41:48: "ZywOo<26><STEAM_1:1:76700232><CT>" [1189 -1878 -416] attacked "s1mple<30><STEAM_1:1:36968273><TERRORIST>" [184 -2133 -416] with "hkp2000" (damage "14") (damage_armor "7") (health "86") (armor "92") (hitgroup "chest")'
        damage_state = DamageState(
            damage=14,
            damage_armor=7,
            health=86,
            armor=92
        )
        expected_result = PlayerAttack(
            attacker="ZywOo",
            victim="s1mple",
            damage_state=damage_state
        )
        result = get_game_object(entry_value)
        self.assertEqual(expected_result, result)

    def test_get_kill_action(self):
        """
        Test parsing of the attack entry
        """
        # pylint: disable=line-too-long
        entry_value = '11/28/2021 - 20:41:49: "ZywOo<26><STEAM_1:1:76700232><CT>" [1186 -1862 -416] killed "s1mple<30><STEAM_1:1:36968273><TERRORIST>" [181 -2121 -370] with "usp_silencer" (headshot)'
        expected_result = PlayerKill(
            attacker="ZywOo",
            victim="s1mple"
        )
        result = get_game_object(entry_value)
        self.assertEqual(expected_result, result)

    def test_game_over(self):
        """
        test catching of the game over event
        """
        # pylint: disable=line-too-long
        entry_value = '11/28/2021 - 21:30:17: Game Over: competitive 1092904694 de_nuke score 6:16 after 50 min'

        result = re.match(MatchRegex.GAME_OVER.value, entry_value)
        self.assertNotEqual(result, None)
