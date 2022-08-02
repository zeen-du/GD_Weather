# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger
from app.api.service import GDService

router = APIRouter()


@router.get(path="/weather")
async def weather(text: str) -> JSONResponse:
    logger.info(f"GET /gd_weather text:{text}")
    address = await GDService.address_format(text)
    if not address:
        response = {"service": 'GD Weather Service', "msg": "请输入更详细的地址"}
        logger.info(f"GET /gd_weather text:{text}, response: {response}")
        return JSONResponse(content=response)
    weather_string = await GDService.weather_format(address)
    response = {"service": 'GD Weather Service', "msg": weather_string}
    logger.info(f"GET /gd_weather text:{text}, response: {response}")
    return JSONResponse(content=response)
