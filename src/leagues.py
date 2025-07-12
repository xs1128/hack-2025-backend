from fastapi import APIRouter
from custom_types import User
from shared_data import users

router = APIRouter()


@router.get("/league/{user_id}")
def get_league(user: User):
    league = sorted(users, key=lambda x: x["quiz"]["solved_quiz"], reverse=True)
    league_position = next(
        (index + 1 for index, u in enumerate(league) if u["id"] == user["id"]), None
    )
    if league_position is None:
        return {"error": "User not found in league"}
    pr = league_position / len(league) * 100
    if pr >= 95:
        rank_name = "松露"
        if pr < 96.5:
            warn = True
    elif pr >= 80:
        rank_name = "蘑菇牛"
        if pr < 84.5:
            warn = True
        elif pr >= 90.5:
            promote = True
    elif pr >= 55:
        rank_name = "蘑菇"
        if pr < 62.5:
            warn = True
        elif pr >= 72.5:
            promote = True
    elif pr >= 20:
        rank_name = "酵母菌"
        if pr < 30.5:
            warn = True
        elif pr >= 44.5:
            promote = True
    else:
        rank_name = "泥土"
        if pr >= 14:
            promote = True
    return {
        "league_position": league_position,
        "pr": pr,
        "rank_name": rank_name,
        "warn": warn if "warn" in locals() else False,
        "promote": promote if "promote" in locals() else False,
    }
