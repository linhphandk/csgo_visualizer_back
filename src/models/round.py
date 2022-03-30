"""
Module contains the objects that
represents all the actions that happened
in that particural round
"""
from abc import ABC
from enum import Enum


class PlayerActionTypes(Enum):
    """
    Enums of player actions
    """
    ATTACK = "ATTACK"
    KILL = "KILL"

class PlayerAction(ABC):
    """
    Represents the action between two players
    """
    action_type: PlayerActionTypes
    attacker: str
    victim: str

    def __init__(self, attacker, victim, action_type):
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
        return "suffered: -"+self.damage+" health, -"+self.armor

    def __eq__(self,other):
        return (
            isinstance(other, DamageState) and
            self.damage == other.damage and
            self.damage_armor == other.damage_armor and
            self.health == other.health and
            self.armor == other.armor
        )

class PlayerKill(PlayerAction):
    """
    Represents the kill actions
    """

    def __init__(self, attacker, victim):
        super().__init__(attacker, victim, PlayerActionTypes.KILL)

    def __str__(self):
        return str(super())

    def __eq__(self, other):
        return (
            isinstance(other, PlayerKill) and
            super().__eq__(other)
        )


class Round:
    """
    Represents all the actions
    taken in a particular round
    """

    def __init__(self):
        self.actions = []

    def add_action(self, action: PlayerAction):
        """
        adds an action to a round
        :param PlayerAction action:
        """
        self.actions.append(action)

    def __str__(self):
        return "Number of actions: "+len(self.actions)
