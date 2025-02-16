"""

This file contains the BaseUniverse object, which represents a Roblox universe ID.
It also contains the UniverseLiveStats object, which represents a universe's live stats.

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from ..badges import Badge

from .baseitem import BaseItem
from ..utilities.shared import ClientSharedObject
from ..utilities.iterators import PageIterator
from ..gamepasses import GamePass
from ..sociallinks import UniverseSocialLink


class UniverseLiveStats:
    """
    Represents a universe's live stats.
    """

    def __init__(self, data: dict):
        self.total_player_count: int = data["totalPlayerCount"]
        self.game_count: int = data["gameCount"]
        self.player_counts_by_device_type: Dict[str, int] = data["playerCountsByDeviceType"]


def _gamepasses_handler(shared: ClientSharedObject, data: dict):
    return GamePass(shared=shared, data=data)


def _universe_badges_handler(shared: ClientSharedObject, data: dict) -> Badge:
    from ..badges import Badge  # Fixme 🥺🥺🥺

    return Badge(shared=shared, data=data)


class BaseUniverse(BaseItem):
    """
    Represents a Roblox universe ID.

    Attributes:
        _shared: The ClientSharedObject.
        id: The universe ID.
    """

    def __init__(self, shared: ClientSharedObject, universe_id: int):
        """
        Arguments:
            shared: The ClientSharedObject.
            universe_id: The universe ID.
        """

        self._shared: ClientSharedObject = shared
        self.id: int = universe_id

    async def get_favorite_count(self) -> int:
        """
        Grabs the universe's favorite count.

        Returns:
            The universe's favorite count.
        """
        favorite_count_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("games", f"v1/games/{self.id}/favorites/count")
        )
        favorite_count_data = favorite_count_response.json()
        return favorite_count_data["favoritesCount"]

    async def is_favorited(self) -> bool:
        """
        Grabs the authenticated user's favorite status for this game.

        Returns:
            Whether the authenticated user has favorited this game.
        """
        is_favorited_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("games", f"v1/games/{self.id}/favorites")
        )
        is_favorited_data = is_favorited_response.json()
        return is_favorited_data["isFavorited"]

    def get_badges(self, limit: int = 10) -> PageIterator:
        """
        Gets the universe's badges.
        """

        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("badges", f"v1/universes/{self.id}/badges"),
            limit=limit,
            handler=_universe_badges_handler,
        )

    async def get_live_stats(self) -> UniverseLiveStats:
        """
        Gets the universe's live stats.
        This data does not update live. These are just the stats that are shown on the website's live stats display.
        """
        stats_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("develop", f"v1/universes/{self.id}/live-stats")
        )
        stats_data = stats_response.json()
        return UniverseLiveStats(data=stats_data)

    def get_gamepasses(self, limit: int = 10) -> PageIterator:
        """
        Gets the universe's gamepasses.
        """

        return PageIterator(
            shared=self._shared,
            url=self._shared.url_generator.get_url("games", f"v1/games/{self.id}/game-passes"),
            limit=limit,
            handler=_gamepasses_handler,
        )

    async def get_social_links(self) -> List[UniverseSocialLink]:
        """

        Gets a universe's social links;

        Returns: A list of the universe's social links.

        """

        links_response = await self._shared.requests.get(
            url=self._shared.url_generator.get_url("games", f"v1/games/{self.id}/social-links/list")
        )
        links_data = links_response.json()["data"]
        return [UniverseSocialLink(shared=self._shared, data=link_data) for link_data in links_data]
