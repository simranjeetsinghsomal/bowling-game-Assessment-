"""
Bowling Game Implementation
===========================

A module for calculating ten-pin bowling game scores.

Design notes
------------
- The game records every roll in a flat list ``self.rolls``.
- The :meth:`score` method iterates frame-by-frame (10 frames total) using an index
  into ``self.rolls``. For each frame it applies the standard bowling rules:
    * Strike: 10 + next two rolls bonus, frame advances by 1 roll.
    * Spare:  10 + next roll bonus, frame advances by 2 rolls.
    * Open:   Sum of the two rolls, frame advances by 2 rolls.
- The 10th frame works naturally because the bonus balls (if any) were already
  appended to ``self.rolls`` and are included only as bonuses for frame 10.
- Basic validation ensures each roll is an integer between 0 and 10.
  (Frame-level pin-count validation is intentionally minimal to keep the focus
   on the scoring kata; comprehensive enforcement can be added later.)

Examples
--------
>>> g = BowlingGame()
>>> for _ in range(12):  # perfect game
...     g.roll(10)
>>> g.score()
300
"""

from __future__ import annotations
from typing import List


class BowlingGame:
    """Represents a single ten-pin bowling game."""

    def __init__(self) -> None:
        """Initialize a new game with no rolls recorded yet."""
        self.rolls: List[int] = []

    def roll(self, pins: int) -> None:
        """Record a single roll.

        Parameters
        ----------
        pins : int
            Number of pins knocked down in this roll. Must be between 0 and 10.

        Raises
        ------
        ValueError
            If ``pins`` is not an integer in the range [0, 10].
        """
        if not isinstance(pins, int):
            raise ValueError("pins must be an integer")
        if pins < 0 or pins > 10:
            raise ValueError("pins must be between 0 and 10 inclusive")
        self.rolls.append(pins)

    def score(self) -> int:
        """Calculate the total score for the current game.

        Returns
        -------
        int
            The total score according to standard ten-pin bowling rules.
        """
        score = 0
        frame_index = 0

        # There are always 10 frames in a game
        for _ in range(10):
            if self._is_strike(frame_index):
                score += 10 + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                score += self._frame_pins(frame_index)
                frame_index += 2
        return score

    # ----- Helper methods -----

    def _is_strike(self, i: int) -> bool:
        """Return True if the roll at index ``i`` is a strike (10 pins)."""
        return i < len(self.rolls) and self.rolls[i] == 10

    def _is_spare(self, i: int) -> bool:
        """Return True if the two rolls starting at index ``i`` sum to 10."""
        return (i + 1) < len(self.rolls) and (self.rolls[i] + self.rolls[i + 1] == 10)

    def _strike_bonus(self, i: int) -> int:
        """Return the bonus for a strike: next two rolls."""
        # Safe access with default 0 for incomplete games
        return self._safe_get(i + 1) + self._safe_get(i + 2)

    def _spare_bonus(self, i: int) -> int:
        """Return the bonus for a spare: next one roll."""
        return self._safe_get(i + 2)

    def _frame_pins(self, i: int) -> int:
        """Return the sum of two rolls for an open frame starting at index ``i``."""
        return self._safe_get(i) + self._safe_get(i + 1)

    def _safe_get(self, i: int) -> int:
        """Return ``self.rolls[i]`` if it exists, else 0 (for unfinished games)."""
        return self.rolls[i] if i < len(self.rolls) else 0
