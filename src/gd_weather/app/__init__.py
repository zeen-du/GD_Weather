# -*- coding: utf-8 -*-
import asyncio

from fastapi import FastAPI

from app.api.config import settings
from app.api.route import router
from app.api.service import GDService, close_client


async def start_up():
    await GDService.init_client()


async def shutdown():
    await close_client()


def create_app() -> FastAPI:
    app = FastAPI(
        title="DG Weather Service",
        version="0.1.0"
    )

    app.include_router(router)
    app.add_event_handler("startup", start_up)
    app.add_event_handler("shutdown", shutdown)

    return app
