import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.storage.database.database import Base

if TYPE_CHECKING:
    from infra.models.user import TelegramUser


class Subscription(Base):
    __tablename__ = "subscription"
    id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    vpn_key: Mapped[str] = mapped_column(String(128), nullable=True)
    vpn_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    traffic: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["TelegramUser"] = relationship(
        "TelegramUser",
        back_populates="subscription",
        uselist=False,
    )
