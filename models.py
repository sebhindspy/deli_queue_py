from pydantic import BaseModel, EmailStr


class Guest(BaseModel):
    email: str  # Using str instead of EmailStr for better compatibility


class QueueStatus(BaseModel):
    is_open: bool
    queue: list[str]
    premium_limit: int
    one_shot_price: int
    venue_mode_enabled: bool
    venue_capacity: int
    guests_in_venue: int
