from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """
    Represents an authenticated client user.

    A new instance is created for each action.
    Immutable once created.
    """

    user_id: str
    token: str

    @property
    def is_authenticated(self) -> bool:
        """
        Returns True if the user has a valid token.
        """
        ...
