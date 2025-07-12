from fastapi import APIRouter
from fastapi import HTTPException
from custom_types import User
from shared_data import users
from pprint import pprint

router = APIRouter()



@router.get("/league/{id}")
def get_league(id: int):

    league = sorted(
        users, 
        key = lambda x: x["quiz"]["solved_quiz"], 
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

    filtered_league = league[max(0, league_position - 10):min(len(league), league_position + 11)]

    league_data = []

    for user in filtered_league:
        league_data.append({
            "user_id": user["id"],
            "league_position": league_position,
            "pr": round((filtered_league.index(user) + 1) / len(filtered_league) * 100),
            "ranking": user["ranking"],
        })

    return league_data
              




    '''判斷（備用）
        warn = False
        promote = False
        if i == league_position:
            if league[i]["ranking"] == 5:
                if pr < 96.5:
                    warn = True
            elif league[i]["ranking"] == 4:
                if pr < 84.5:
                    warn = True
                elif pr >= 90.5:
                    promote = True
            elif league[i]["ranking"] == 3:
                if pr < 62.5:
                    warn = True
                elif pr >= 72.5:
                    promote = True
            elif league[i]["ranking"] == 2:
                if pr < 30.5:
                    warn = True
                elif pr >= 44.5:
                    promote = True
            else:
                if pr >= 14:
                    promote = True
        '''

