from datetime import datetime
from custom_types import User
from shared_data import users
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()


# Simple authentication endpoint
@router.post("/user")
# TODO: add default val and error handling
def login(email: str):
    if not email:
        raise HTTPException(status_code=400, detail="Invalid name and email format")

    for user in users:
        if email == user["email"]:
            return {"user": user}

    id = len(users)

    new_user: User = {
        "id": id,
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
    return RedirectResponse("http://127.0.0.1:8000/user/setup?id=", id)


@router.post("/user/setup")
def register_user(id: str):
    # Register success, redirect to game page
    ...
