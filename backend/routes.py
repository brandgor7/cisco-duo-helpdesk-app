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

from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel
from logrr import logger_manager
from duo_app import duo_authenticator

router = APIRouter()


class UserRequest(BaseModel):
    email: str


# Using duo_app.py
@router.post("/authenticate/")
def authenticate(user_request: UserRequest):
    try:
        logger_manager.console.print('[orange1]Authenticating with Duo...[/orange1]')
        result = duo_authenticator.authenticate_user(user_request.email)
        # result = duo_authenticator.parse_hostname(config.DUO_API_URL)
        logger_manager.console.print(f'Result {result}')
        return {"output": result}
    except Exception as e:
        # Log and handle the error
        logger_manager.console.print(f"[red]Error: {e}[/red]")
        raise HTTPException(status_code=500, detail=str(e))