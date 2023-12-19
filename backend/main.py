"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import config
from logrr import logger_manager
from routes import router as webhook_router
import uvicorn


def create_app() -> FastAPI:
    fastapi_app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)

    # Configure CORS
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @fastapi_app.on_event("startup")
    async def on_startup():
        logger_manager.print_start_panel(config.APP_NAME)
        logger_manager.display_config_table(config)  # Display the configuration table using the new function

    @fastapi_app.on_event("shutdown")
    async def on_shutdown():
        logger_manager.print_exit_panel()

    fastapi_app.include_router(webhook_router)
    return fastapi_app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="warning", reload=True)
