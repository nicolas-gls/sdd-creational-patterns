from abc import ABC, abstractmethod
from uuid import uuid4
from .budget import GlobalBudget
from .campaign import Campaign


class ChannelClient(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def create_campaign(self, campaign: Campaign) -> str: ...

    @abstractmethod
    def pause_campaign(self, campaign_id: str) -> None: ...


class GoogleAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("google")

    def create_campaign(self, campaign: Campaign) -> str:
        budget = GlobalBudget()
        budget.allocate(campaign.daily_budget)
        return f"g-{uuid4().hex[:8]}"

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[GoogleAds] Pausing campaign {campaign_id}")


class FacebookAdsClient(ChannelClient):
    def __init__(self):
        super().__init__("facebook")

    def create_campaign(self, campaign: Campaign) -> str:
        budget = GlobalBudget()
        budget.allocate(campaign.daily_budget)
        return f"f-{uuid4().hex[:8]}"

    def pause_campaign(self, campaign_id: str) -> None:
        print(f"[FacebookAds] Pausing campaign {campaign_id}")


class ChannelClientFactory:
    """Maps a channel name to the client class that knows how to build it."""

    _registry = {
        "google": GoogleAdsClient,
        "facebook": FacebookAdsClient,
    }

    @staticmethod
    def create(channel: str) -> ChannelClient:
        client_cls = ChannelClientFactory._registry.get(channel.lower())
        if client_cls is None:
            raise ValueError(f"Unknown channel: {channel!r}")
        return client_cls()
