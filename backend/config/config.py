"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at https://developer.cisco.com/docs/licenses.
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import pathlib
import re
from typing import Optional, ClassVar
from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings


# Dynamically locate the .env file and handle cases where it might not exist.
try:
    env_path = pathlib.Path(__file__).parents[0] / '.env'
    load_dotenv(dotenv_path=env_path)
    # print(f'env path: {env_path}')  # for debugging
except FileNotFoundError:
    print("Warning: .env file not found.")


class Config(BaseSettings):
    # Class constants
    DIR_PATH: ClassVar[pathlib.Path] = pathlib.Path(__file__).parents[0]
    ENV_FILE_PATH: ClassVar[str] = str(DIR_PATH / '.env')

    # Optional Project Settings (used for docs)
    APP_VERSION: Optional[str] = None
    APP_NAME: Optional[str] = 'Add an app name in .env'
    LOGGER_LEVEL: Optional[str] = 'DEBUG'

    # Backend
    DUO_API_URL: str
    DUO_IKEY: str
    DUO_SKEY: str


    @field_validator('DUO_API_URL', mode='before')
    def validate_duo_api_url(cls, v):
        if not re.match(r'https://api-16b8c3ed\.duosecurity\.com', v):
            raise ValueError('DUO_API_URL must be: https://api-16b8c3ed.duosecurity.com')
        return v


config = Config()      # Create a single instance of Config()
