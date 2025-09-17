from datetime import datetime
from typing import Any

from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func


class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()


class TimestampMixin:
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now())
