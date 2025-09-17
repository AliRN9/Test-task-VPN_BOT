from dataclasses import dataclass
from typing import Callable, Awaitable

from sqlalchemy.ext.asyncio import AsyncSession




@dataclass
class BaseRepo:
    """
    A class representing a base repository for handling database operations.

    Attributes:
        db_session (AsyncSession): The database session used by the repository.

    """

    db_session: AsyncSession
