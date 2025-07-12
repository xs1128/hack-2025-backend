from fastapi import APIRouter
from custom_types import User
from shared_data import users
from datetime import datetime

router = APIRouter()
today = datetime.now().date()

@router.post("/internal/streak")
def streak():
    for i in range(len(users)): 
        if users[i]["store"]["freeze"] >= 1:
            users[i]['store']['freeze'] -= 1
        elif users[i]["quiz"]["last_played"].date() == today:
            users[i]["quiz"]["current_streak"] += 1
        else:
            users[i]["quiz"]["current_streak"] = 0
    return

@router.post("/did_today/{id}")
def did_or_not(id: int):
    if users[id]["quiz"]["last_played"].date() == today:
        return 1
    else:
        return 0