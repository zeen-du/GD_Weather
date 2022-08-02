# -*- coding: utf-8 -*-
import sys
from os.path import abspath, dirname

sys.path.insert(0, abspath(dirname(__file__)))

from app import create_app
from app.api.config import settings
from app.api.log import logger

if __name__ == '__main__':
    import uvicorn
    import argparse

    app = create_app()
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=settings.port, help='service port')
    args = parser.parse_args()
    logger.info(f"Start Server Host: {settings.host} Port: {settings.port}")
    uvicorn.run(app, host=settings.host, port=args.port)
