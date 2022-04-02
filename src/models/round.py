"""
Module contains the objects that
represents all the actions that happened
in that particural round
"""
from abc import ABC
from enum import Enum
from typing import List
class TeamSide(Enum):
    """
    Names of teams people can join
    """
    CT = "CT"
    TERRORIST = "TERRORIST"
    UNASSIGNED = "Unassigned"
    SPECTATOR = "Spectator"

class PlayerActionTypes(Enum):
    """
    Enums of player actions
    """
    ATTACK = "ATTACK"
    KILL = "KILL"
    ASSIST = "ASSIST"

class PlayerAction(ABC):
    """
    Represents the action between two players
    """
    action_type: PlayerActionTypes
    attacker: str
    victim: str

    def __init__(
        self,
        attacker:str,
        victim:str,
        action_type:PlayerActionTypes
    ):
        self.action_type = action_type
        self.attacker = attacker
        self.victim = victim

    def __str__(self):
        return self.attacker+" "+self.action_type.value+" "+self.victim
    def __eq__(self, other):
        return (
            isinstance(other, PlayerAction) and
            other.attacker == self.attacker and
            other.victim == self.victim and
            other.action_type == self.action_type
        )

    def serialize(self):
        """
        function that return serialized
        object
        """
        serialized = vars(self)
        serialized["action_type"] = self.action_type.value

        return vars(self)


class PlayerAttack(PlayerAction):
    """
    Represents the attack on a player
    """

    def __init__(
        self,
        attacker,
        victim,
        damage_state
    ):
        super().__init__(attacker, victim, PlayerActionTypes.ATTACK)
        self.damage_state = damage_state

    def __str__(self):
        return str(super())

    def __eq__(self, other):
        return (
            isinstance(other, PlayerAttack) and
            super().__eq__(other) and
            self.damage_state == other.damage_state
        )
    def serialize(self):
        serialized = { **super().serialize(),**vars(self)}
        serialized["damage_state"] = vars(self.damage_state)
        return serialized

class DamageState:
    """
    Class that represents
    armor, health status and
    damage dealt
    """

    def __init__(self, damage,damage_armor,health,armor):
        self.damage = damage
        self.damage_armor = damage_armor
        self.health = health
        self.armor = armor

    def __str__(self):
        return "suffered: -"+str(self.damage)+" health, -"+str(self.armor)

    def __eq__(self,other):
        return (
            isinstance(other, DamageState) and
            self.damage == other.damage and
            self.damage_armor == other.damage_armor and
            self.health == other.health and
            self.armor == other.armor
        )

    def serialize(self):
        """
        returns serialized object
        """
        return vars(self)

class PlayerKill(PlayerAction):
    """
    Represents the kill actions
    """
    headshot:bool
    def __init__(self, attacker, victim, headshot=False):
        super().__init__(attacker, victim, PlayerActionTypes.KILL)
        self.headshot = headshot

    def __str__(self):
        return str(super())

    def __eq__(self, other):
        return (
            isinstance(other, PlayerKill) and
            super().__eq__(other) and
            self.headshot == other.headshot
        )

class PlayerAssist(PlayerAction):
    """
    Represents the assist actions
    """

    def __init__(self, attacker, victim):
        super().__init__(attacker, victim, PlayerActionTypes.ASSIST)

    def __eq__(self, other):
        return (
            isinstance(other, PlayerAssist) and
            super().__eq__(other)
        )


class Round:
    """
    Represents all the actions
    taken in a particular round
    """

    def __init__(self):
        self.actions = []
        self.result = {
            "ct": 0,
            "t": 0,
        }

    def add_action(self, action: PlayerAction):
        """
        adds an action to a round
        :param PlayerAction action:
        """
        self.actions.append(action)

    def __str__(self):
        return "Number of actions: "+len(self.actions)

    def serialize(self):
        """
        returns serialized object
        """
        return {
            "result": self.result,
            "actions": [action.serialize() for action in self.actions]
        }

    def set_result(self, ct_score:int,t_score:int):
        """
        sets the score
        """
        self.result = {
            "ct": ct_score,
            "t": t_score
        }

class Team:
    """
    Class representing CTs or Terrorists
    """
    name:str
    members: List[str]
    start_side: TeamSide
    

    def __init__(self,start_side:TeamSide):
        self.start_side = start_side
        self.members = []
        self.name = ""

    def add_member(self,name:str):
        """
        Adds a team member
        """
        self.members.append(name)

    def remove_member(self,name:str):
        """
        Removes a team member
        """
        self.members.remove(name)

    def set_name(self,name):
        """
        sets the name of the Team
        """
        self.name = name

    def serialize(self):
        """
        serializes the object to dict
        """
        result = vars(self)
        result["start_side"] = result["start_side"].value
        return result
