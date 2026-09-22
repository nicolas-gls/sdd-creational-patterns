from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any, List


@dataclass(frozen=True)
class Campaign:
    name: str
    channel: str
    daily_budget: float
    start_date: date
    end_date: Optional[date]
    target_audience: Dict[str, Any]
    creatives: List[Dict[str, str]]
    tracking: Dict[str, str]


class CampaignBuilder:
    def __init__(self):
        self.name = ""
        self.channel = ""
        self.daily_budget = 0.0
        self.start_date = None
        self.end_date = None
        self.target_audience = {}
        self.creatives = []
        self.tracking = {}

    def with_name(self, name: str):
        self.name = name
        return self

    def with_channel(self, channel: str):
        self.channel = channel
        return self

    def with_budget(self, daily_budget: float):
        self.daily_budget = daily_budget
        return self

    def with_dates(self, start_date, end_date=None):
        self.start_date = start_date
        self.end_date = end_date
        return self

    def with_audience(self, **kwargs):
        self.target_audience.update(kwargs)
        return self

    def add_creative(self, headline: str, image_url: str):
        self.creatives.append({"headline": headline, "image_url": image_url})
        return self

    def with_tracking(self, **kwargs):
        self.tracking.update(kwargs)
        return self

    def build(self) -> Campaign:
        if not self.name:
            raise ValueError("Campaign must have a name.")
        if not self.channel:
            raise ValueError("Campaign must have a channel.")
        if self.daily_budget <= 0:
            raise ValueError("Daily budget must be provided and greater than zero.")
        if not self.start_date:
            raise ValueError("Start date is required.")
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("Start date cannot be later than end date.")
        if not self.creatives:
            raise ValueError("At least one creative is required.")

        return Campaign(
            name=self.name,
            channel=self.channel,
            daily_budget=self.daily_budget,
            start_date=self.start_date,
            end_date=self.end_date,
            target_audience=dict(self.target_audience),
            creatives=[dict(creative) for creative in self.creatives],
            tracking=dict(self.tracking),
        )
