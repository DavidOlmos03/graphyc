"""Module that defines restriction data structures and a manager.

A restriction is treated as: (a) * x1 + (b) * x2 (op) c
Where op is '≤' or '≥'.
"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Restriction:
    """
    Immutable representation of a linear restriction.

    Attributes
    ----------
    a : float
        Coefficient for x1.
    b : float
        Coefficient for x2.
    op : str
        Operator: '≤' or '≥'.
    c : float
        Right hand side constant.
    """
    a: float
    b: float
    op: str # "≤" or "≥"
    c: float


class RestrictionManager:
    """Manages a collection of restrictions."""
    
    def __init__(self):
        self.restrictions = []
    
    def add(self, restriction: Restriction) -> None:
        """Add a restriction to the manager."""
        self.restrictions.append(restriction)
    
    def clear(self) -> None:
        """Clear all restrictions."""
        self.restrictions.clear()
    
    def get_all(self) -> list:
        """Get all restrictions."""
        return self.restrictions.copy()
