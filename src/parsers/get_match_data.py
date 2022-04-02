"""
Module contains logic for extracting data
based on game data from a face it server
"""
from typing import Union, Optional
from pathlib import Path
from enum import Enum
import re

from src.models.round import (
    Round,
    PlayerKill,
    PlayerAttack,
    DamageState,
    PlayerAssist,
    Team,
    TeamSide
)
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
    PLAYER_ASSIST = get_extended_regex(PLAYER_TAG_WITH_TEAM_REGEX+" assisted killing " + PLAYER_TAG_WITH_TEAM_REGEX)
    GAME_OVER = get_extended_regex("Game Over: competitive .*")
    TEAM_SWITCH = get_extended_regex(r"\""+PLAYER_TAG_REGEX+r"\" switched from team \<(CT|TERRORIST|Unassigned|Spectator)\> to \<(CT|TERRORIST|Unassigned|Spectator)\>")
    TEAM_SCORE = get_extended_regex(r"Team \"(TERRORIST|CT)\" triggered \"SFUI_Notice_(Target_Bombed|Terrorists_Win|CTs_Win|Bomb_Defused)\" \(C?T \"(\d+)\"\) \(C?T \"(\d+)\"\)")
    MATCH_STATUS = get_extended_regex(r"MatchStatus: Team playing \"(CT|TERRORIST)\": (.*)")
def get_game_data(data_path: Path):
    """
    reads the data from the imput file
    and then returns round objects
    """
    match_start = False
    rounds_list = []
    new_round = None
    teams = {
        "CT": Team(TeamSide.CT),
        "TERRORIST": Team(TeamSide.TERRORIST),
        "Unassigned":Team(TeamSide.UNASSIGNED),
        "Spectator":Team(TeamSide.SPECTATOR)
    }
    with open(data_path,'r', encoding='utf-8') as data:
        for match_entry in data:
            result = re.search(MatchRegex.TEAM_SWITCH.value, match_entry)

            if result is not None and not match_start:
                if result.group(3) not in ["Spectator", "Unassigned"]:
                    teams[result.group(3)].add_member(result.group(1))

                #remove if exist in other team
                if result.group(1) in teams[result.group(2)].members:
                    teams[result.group(2)].remove_member(result.group(1))


            # The match should not begin before
            # the [FACEIT^] LIVE entry so ignore
            # before that
            if re.match(MatchRegex.FACE_IT_LIVE.value, match_entry):
                match_start = True

            result = re.match(MatchRegex.MATCH_STATUS.value, match_entry)

            if result and not match_start:
                teams[result.group(1)].set_name(result.group(2))
            if not match_start:
                continue

            if re.match(MatchRegex.ROUND_START.value, match_entry):
                new_round = Round()
            
            game_action = get_game_object(match_entry)

            if(
                game_action is not None and
                new_round is not None
            ):
                new_round.add_action(game_action)

            result = re.match(MatchRegex.TEAM_SCORE.value, match_entry)
            if (
                result is not None and
                new_round is not None
            ):
                new_round.set_result( int(result.group(3)), int(result.group(4)))
            if re.match(MatchRegex.ROUND_END.value, match_entry):
                rounds_list.append(new_round)
            if re.match(MatchRegex.GAME_OVER.value, match_entry):
                break

    # switch the teams so at the moment
    # the sides are based on the end of the game
    return {
        "round_list": rounds_list,
        "teams": [
            teams["TERRORIST"].serialize(),
            teams["CT"].serialize(),
        ]
    }

GameObjectType = Union[PlayerAttack,PlayerKill, PlayerAssist]


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
            victim=result.group(3),
            headshot=bool(result.group(5)),
        )

    result = re.search(MatchRegex.PLAYER_ASSIST.value, game_entry)
    if result:
        return PlayerAssist(
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
