# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from app.api.service import GDService
from app.api.config import settings

router = APIRouter()


@router.get(path="/weather")
async def weather(text: str, token: str = Header(default=None)) -> JSONResponse:
    logger.info(f"GET /weather text:{text}")
    if token != settings.token:
        raise HTTPException(status_code=401, detail="Invalid Token")
    address = await GDService.address_format(text)
    if not address:
        response = {"service": 'GD Weather Service', "msg": "请输入更详细的地址"}
        logger.info(f"GET /weather text:{text}, response: {response}")
        return JSONResponse(content=response)
    weather_string = await GDService.weather_format(address)
    response = {"service": 'GD Weather Service', "msg": weather_string}
    logger.info(f"GET /weather text:{text}, response: {response}")
    return JSONResponse(content=response)
