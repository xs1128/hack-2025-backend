from fastapi import APIRouter
from fastapi import HTTPException
from shared_data import users

router = APIRouter()


@router.get("/league/{id}")
def get_league(id: int):

    league = sorted(
        users,
        key=lambda x: x["quiz"]["solved_quiz"],
        reverse=True
    )

    league_position = None

    for i in range(len(league)):
        if league[i]["id"] == id:
            print(id)
            league_position = i
            break

    if league_position is None:
        raise HTTPException(status_code=404, detail="User not found in league")

    league = list(filter(
        lambda x: x["ranking"] == users[league_position]["ranking"],
        league
    ))

    filtered_league = league[max(
        0, league_position - 10):min(len(league), league_position + 11)]

    league_data = []

    for user in filtered_league:
        league_data.append({
            "user_id": user["id"],
            "league_position": league_position,
            "pr": round((filtered_league.index(user) + 1) / len(filtered_league) * 100),
            "ranking": user["ranking"],
        })

    return league_data
