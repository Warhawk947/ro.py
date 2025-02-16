"""

This file contains the BaseRole object, which represents a Roblox role ID.

"""

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject


class BaseRole(BaseItem):
    """
    Represents a Roblox role ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The role ID.
    """

    def __init__(self, shared: ClientSharedObject, role_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            role_id: The role ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = role_id
