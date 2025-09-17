from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class UserCreateShema(BaseModel):
    tg_user_id: int
    username: Optional[str] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    referral_link: Optional[str] = None

    @field_validator("referral_link", mode="before")
    @classmethod
    def default_ref(cls, v: Optional[str]):
        v = (v or "").strip()
        return v or "start"


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    tg_user_id: int
    username: Optional[str] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    referral_link: str
