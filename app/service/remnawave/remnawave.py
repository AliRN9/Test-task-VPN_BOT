import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

import aiohttp

from app.exceptions import RemnawaveError


class RemnawaveClient:
    def __init__(self, api_token: str, base_url: str = "https://cdn.remna.st/api", timeout: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

    @staticmethod
    def _iso(dt: Optional[datetime]) -> Optional[str]:
        if not dt:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()

    async def create_user(
            self,
            *,
            username: str,
            status: str = "ACTIVE",
            traffic_limit_bytes: int = 0,
            traffic_limit_strategy: str = "NO_RESET",
            expire_at: Optional[datetime],
            created_at: Optional[datetime],
            description: str = "",
            tag: Optional[str] = None,
            telegram_id: Optional[int] = None,

    ) -> Dict[str, Any]:
        # await self.register_service()
        # Тут я получаю 401 ошибку авторизации(долго мучался, но видимо надо как то зарегаться)
        payload = {
            "username": username,
            "status": status,
            "trafficLimitBytes": int(traffic_limit_bytes),
            "trafficLimitStrategy": traffic_limit_strategy,
            "expireAt": self._iso(expire_at),
            "createdAt": self._iso(created_at),
            "description": description,
            "tag": tag,
            "telegramId": telegram_id,

        }
        logging.info(f"payload: {payload}")
        logging.info(f"headers: {self._headers()}")
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as client:
            async with client.post(f"{self.base_url}/users", headers=self._headers(), json=payload) as response:
                # request.raise_for_status()
                if response.status == 201:
                    return await response.json(content_type=None)
                else:
                    try:
                        error_data = await response.json(content_type=None)
                    except aiohttp.ContentTypeError:
                        error_data = await response.text()[:1000]
                    raise RemnawaveError(response.status, error_data)

    async def register_service(self):
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as client:
            async with client.post("https://cdn.remna.st/api/auth/register",
                                   headers={
                                       "Content-Type": "application/json"
                                   },
                                   json={
                                       "username": "TEst_Test_Test",
                                       "password": "TEst_Test_Test.12123"
                                   }
                                   ) as request:
                request.raise_for_status()

                data = await request
                logging.info(f"response: {data}")
