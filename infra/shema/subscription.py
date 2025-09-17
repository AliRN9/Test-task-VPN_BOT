from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubscriptionShema(BaseModel):
    user_id: int
    vpn_id: UUID
    vpn_key: Optional[str] = None
    subscription_date: Optional[datetime] = None
    traffic: int = 0
    model_config = ConfigDict(from_attributes=True)


class SubscriptionUpdateShema(BaseModel):
    vpn_id: Optional[UUID] = None
    vpn_key: Optional[str] = None
    subscription_date: Optional[datetime] = None
    traffic: Optional[int] = None
