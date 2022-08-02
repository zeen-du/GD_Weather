import asyncio
import datetime
from typing import Dict, List, Optional

from aiohttp import ClientSession, TCPConnector
from fastapi.exceptions import HTTPException
from loguru import logger
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.api.config import settings
from app.api.constant import GEO_URL, WEATHER_URL, POI_URL
from app.api.payload import POIModel, WeatherModel

HTTP_TIME_OUT = 20


class BaseHttpClient:
    clients: List["BaseHttpClient"] = []

    def __init__(self, default_timeout=HTTP_TIME_OUT):
        self.session: Optional[ClientSession] = None
        self.default_timeout: int = default_timeout

        self.session = ClientSession(
            connector=TCPConnector(enable_cleanup_closed=True),
        )

        self.clients.append(self)

    async def close(self):
        await self.session.close()


async def close_client():
    for client in BaseHttpClient.clients:
        await client.close()


class _GDService:
    def __init__(self):
        self.client = None  # type: BaseHttpClient
        self.headers = None

    async def init_client(self):
        self.client = BaseHttpClient()

    async def async_poi(self, text, city=None, retry=3) -> Optional[POIModel]:
        if city:
            params = {"key": settings.gd_api_key, "offset": 10, "keywords": text, "city": city}
        else:
            params = {"key": settings.gd_api_key, "offset": 10, "keywords": text}
        for i in range(retry):
            try:
                logger.info(f"Get Poi: {text}")
                async with self.client.session.get(url=POI_URL, timeout=HTTP_TIME_OUT, params=params) as resp:
                    data = await resp.json()
                    pois = data.get("pois")[0]
                    if not pois:
                        if data["suggestion"]["cities"]:
                            pois = [{"address": text}]
                    resp = POIModel(**pois)
                    logger.info(f"Get Poi: {text}, Return: {resp}")
                    return resp
            except BaseException as e:
                logger.exception(e)
            return

    async def geo(self, text, city=None, retry=3) -> Optional[POIModel]:
        if city:
            params = {"key": settings.gd_api_key, "offset": 10, "address": text, "city": city}
        else:
            params = {"key": settings.gd_api_key, "offset": 10, "address": text}
        for i in range(retry):
            try:
                async with self.client.session.get(url=GEO_URL, timeout=HTTP_TIME_OUT, params=params) as resp:
                    logger.info(f"Get Geo: {text}")
                    data = await resp.json()
                    poi_data = data["geocodes"]
                    if not poi_data:
                        return
                    poi_format = {
                        "pname": poi_data[0].get("province") or "",
                        "cityname": poi_data[0].get("city") or "",
                        "adname": poi_data[0].get("district") or "",
                        "address": poi_data[0].get("formatted_address") or "",
                        "name": poi_data[0].get("formatted_address") or "",
                        "location": poi_data[0].get("location") or "",
                        "level": poi_data[0].get("level") or "",
                        "adcode": poi_data[0].get("adcode") or ""
                    }
                    resp = POIModel(**poi_format)
                    logger.info(f"Get Goi: {text}, Return: {resp}")
                    return resp
            except BaseException as e:
                logger.exception(e)

    async def get_weather(self, info: POIModel, extensions="base", retry=3) -> Optional[WeatherModel]:
        params = {"key": settings.gd_api_key, "offset": 10, "city": info.adcode, "extensions": extensions}
        for i in range(retry):
            try:
                async with self.client.session.get(url=WEATHER_URL, timeout=HTTP_TIME_OUT, params=params) as resp:
                    logger.info(f"Get Weather: {info.complete_address}")
                    data = await resp.json()
                    weather_data = data
                    if not weather_data:
                        return
                    resp = WeatherModel(**weather_data)
                    logger.info(f"Get Weather: {info.complete_address}, Return: {resp}")
                    return resp
            except BaseException as e:
                logger.exception(e)

    async def address_format(self, text):
        model = await self.async_poi(text)
        if not model:
            return
        poi_model = await self.geo(text=model.complete_address)
        return poi_model

    async def weather_format(self, info: POIModel) -> str:
        live_model = await self.get_weather(info, "base")
        forecast_model = await self.get_weather(info, "all")
        lives = live_model.lives[0]
        forecasts = forecast_model.forecasts[0]
        lives_str = lives.format_str(lives.dict())
        forecasts_str = forecasts.format_str(forecasts.dict())
        update_time_str = f"更新时间: {lives.reporttime}"
        return lives_str + forecasts_str + update_time_str


GDService = _GDService()

if __name__ == '__main__':
    async def run():
        await GDService.init_client()
        address = await GDService.address_format("庄头镇")
        resp = await GDService.weather_format(address)
        print(resp)
        await close_client()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
