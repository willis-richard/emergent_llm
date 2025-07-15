"""Actions for game theory experiments.
Reuses axelrod's Action enum for consistency.
"""
from axelrod import Action
from axelrod.action import actions_to_str, str_to_actions, UnknownActionError

# Export the actions for convenience
C, D = Action.C, Action.D

__all__ = ['Action', 'C', 'D', 'actions_to_str', 'str_to_actions', 'UnknownActionError']
