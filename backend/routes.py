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
from typing import List, Optional
from pydantic import BaseModel
from logrr import logger_manager
from duo_app import duo_authenticator

router = APIRouter()


class Device(BaseModel):
    id: str
    type: str
    capabilities: List[str]
    model: Optional[str] = None
    number: Optional[str] = None


class User(BaseModel):
    username: str
    fullname: str
    email: Optional[str] = None
    status: str
    devices: List[Device]


@router.post("/authenticate/")
async def authenticate(user_request: User):
    try:
        user_request_dict = user_request.model_dump()  # Convert the user_request object to a dictionary
        result = duo_authenticator.authenticate_user(user_request_dict)  # Pass the user_request_dict to the authenticate_user function
        # Simulate authentication result for demonstration purposes (optional)
        # result = "Authentication successful for user: " + user_request.username
        return {"output": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Log and handle the error


@router.get("/users/")
def users():
    try:
        logger_manager.console.print('[orange1]Fetching users...[/orange1]')
        result = duo_authenticator.fetch_users()
        return {"output": result}
    except Exception as e:
        # Log and handle the error
        logger_manager.console.print(f"[red]Error: {e}[/red]")
        raise HTTPException(status_code=500, detail=str(e))
