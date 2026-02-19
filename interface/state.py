from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict

from invariants import Invariants


@dataclass
class AppState:
    """
    In-memory application state for the CLI interface.

    Maintains:
    - counter → menu mapping
    - invariant checks
    """

    counter: int = 0
    menu: Dict[int, Callable] = field(default_factory=dict)
    inv: Invariants = field(default_factory=Invariants)

    def assert_ok(self) -> None:
        """
        Validate that state invariants hold.
        """
        ...

    def register(self, fn: Callable) -> int:
        """
        Increment counter and map it to a callable action.

        Returns:
            int → menu option number
        """
        ...

    def get(self, choice: int) -> Callable | None:
        """
        Retrieve callable mapped to menu selection.
        """
        ...

    def reset(self) -> None:
        """
        Reset state to initial values.
        """
