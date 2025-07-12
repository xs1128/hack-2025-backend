from datetime import datetime

from starlette.types import HTTPExceptionHandler
from custom_types import User
from shared_data import users
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import re
router = APIRouter()


# Simple authentication endpoint
@router.post("/user")
def login(email: str):
    if not email:
        raise HTTPException(
            status_code=400, detail="Invalid name and email format")
    elif re.match(r'^[a-zA-Z0–9._%+-]+@[a-zA-Z0–9.-]+\.[a-zA-Z]{2,}$', email) is None:
        raise HTTPException(status_code=422, detail="Invalid email")

    for user in users:
        if email == user["email"]:
            return {"user": user}

    _id = len(users)

    new_user: User = {
        "id": _id,
        "name": None,
        "email": email,
        "created_at": datetime.now(),
        "quiz": {
            "current_id": 1,
            "last_played": datetime.now(),
            "current_streak": 0,
            "solved_quiz": 0,
        },
        "store": {
            "coin": 0,
            "freeze": 0,
        },
    }

    users.append(new_user)
    return {"user": users[_id]}


@router.post("/user/setup/{_id}")
def register_user(_id: int, name: str):
    try:
        users[_id]["name"] = name
        return {"user": users[_id]}
    except IndexError as err:
        raise HTTPException(status_code=400, detail=f"{err}")
