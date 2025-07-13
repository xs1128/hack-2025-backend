from fastapi import APIRouter, HTTPException, Response
from custom_types import User
from shared_data import users
from datetime import datetime

router = APIRouter()


@router.post("/internal/conclude-streak")
def streak():
    today = datetime.now().date()
    for i in range(len(users)):
        last_played = users[i]["quiz"]["last_played"]
        if last_played is not None and last_played.date() == today:
            pass
        elif users[i]["store"]["freeze"] >= 1:
            users[i]["store"]["freeze"] -= 1
        else:
            users[i]["quiz"]["current_streak"] = 0
    return Response(status_code=204)


@router.get("/streak-stat/{id}")
def streak_status(id: int):
    today = datetime.now().date()
    user = None
    for user in users:
        if user["id"] == id:
            user = user
            break
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    user_last_played = user["quiz"]["last_played"]
    return {
        "current_streak": user["quiz"]["current_streak"],
        "today_completed": (
            user_last_played is not None and user_last_played.date() == today
        ),
    }
