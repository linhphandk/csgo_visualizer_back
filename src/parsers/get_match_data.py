"""
Module contains logic for extracting data
based on game data from a face it server
"""
from typing import Union, Optional
from pathlib import Path
from enum import Enum
import re

from src.models.round import Round, PlayerKill, PlayerAttack, DamageState
PLAYER_TAG_REGEX = r"(.+)<\d+><.+>"
PLAYER_TAG_WITH_TEAM_REGEX = r"\""+PLAYER_TAG_REGEX+"<(CT|TERRORIST|Unassigned|Spectator|)>\""
POSITION_REGEX = r"\[-?\d+ -?\d+ -?\d+\]"


def get_extended_regex(regex: str):
    """
    Adds the date time and begining and end of line chars
    """
    return r"^\d+\/\d+\/\d+ - \d+:\d+:\d+: "+regex+"$"

# pylint: disable=line-too-long
class MatchRegex(Enum):
    """
    Enum holding regular expressions for
    match entries
    """
    FACE_IT_LIVE = get_extended_regex(r" \[FACEIT\^] LIVE!")
    ROUND_START = get_extended_regex("World triggered \"Round_Start\"")
    ROUND_END = get_extended_regex("World triggered \"Round_End\"")
    PLAYER_KILL = get_extended_regex(PLAYER_TAG_WITH_TEAM_REGEX+" "+POSITION_REGEX+" killed " +
                                     PLAYER_TAG_WITH_TEAM_REGEX+" "+POSITION_REGEX+r" with \"\w+\"( \(headshot\))?")
    PLAYER_ATTACK = get_extended_regex(PLAYER_TAG_WITH_TEAM_REGEX+" "+POSITION_REGEX+" attacked " + PLAYER_TAG_WITH_TEAM_REGEX+" "+POSITION_REGEX +
                                       r" with \"\w+\" \(damage \"(\d+)\"\) \(damage_armor \"(\d+)\"\) \(health \"(\d+)\"\) \(armor \"(\d+)\"\) \(hitgroup \"(\w+)\"\)")
    GAME_OVER = get_extended_regex("Game Over: competitive .*")
    TEAM_SWITCH = get_extended_regex(r"\""+PLAYER_TAG_REGEX+r"\" switched from team \<(CT|TERRORIST|Unassigned|Spectator)\> to \<(CT|TERRORIST|Unassigned|Spectator)\>")

def get_game_data(data_path: Path):
    """
    reads the data from the imput file
    and then returns round objects
    """
    match_start = False
    rounds_list = []
    new_round = None
    teams = {
        "CT":[],
        "TERRORIST":[],
        "Unassigned":[],
        "Spectator":[]
    }
    with open(data_path,'r', encoding='utf-8') as data:
        for match_entry in data:
            if re.match(MatchRegex.TEAM_SWITCH.value, match_entry):
                res = re.search(MatchRegex.TEAM_SWITCH.value, match_entry)
                if res.group(3) not in ["Spectator", "Unassigned"]:
                    teams[res.group(3)].append(res.group(1))

                #remove if exist in other team
                if res.group(1) in teams[res.group(2)]:
                    teams[res.group(2)].remove(res.group(1))


            # The match should not begin before
            # the [FACEIT^] LIVE entry so ignore
            # before that
            if re.match(MatchRegex.FACE_IT_LIVE.value, match_entry):
                match_start = True

            if not match_start:
                continue

            if re.match(MatchRegex.ROUND_START.value, match_entry):
                new_round = Round()

            if not match_start:
                continue

            result = get_game_object(match_entry)

            if result and new_round is not None:
                new_round.add_action(result)

            if re.match(MatchRegex.ROUND_END.value, match_entry):
                rounds_list.append(new_round)
            if re.match(MatchRegex.GAME_OVER.value, match_entry):
                break

    # switch the teams so at the moment
    # the sides are based on the end of the game
    return {
        "round_list": rounds_list,
        "teams": {
            "CT": teams["TERRORIST"],
            "TERRORIST": teams["CT"],
        }
    }

GameObjectType = Union[PlayerAttack,PlayerKill]


def get_game_object(game_entry) -> Optional[GameObjectType]:
    """
    gets the string defining the entity of a match
    and return the a specific class containing extracted
    information
    """
    result = re.search(MatchRegex.PLAYER_KILL.value, game_entry)
    if result:
        return PlayerKill(
            attacker=result.group(1),
            victim=result.group(3)
        )

    result = re.search(MatchRegex.PLAYER_ATTACK.value, game_entry)

    if result:
        damage_state = DamageState(
            damage=int(result.group(5)),
            damage_armor=int(result.group(6)),
            health=int(result.group(7)),
            armor=int(result.group(8))
        )
        return PlayerAttack(
            attacker=result.group(1),
            victim=result.group(3),
            damage_state = damage_state
        )
    return None


if __name__ == "__main__":
    get_game_data(Path('./src/assets/data.txt'))
