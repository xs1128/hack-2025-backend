from fastapi import APIRouter
from fastapi import HTTPException
from custom_types import User
from shared_data import users

router = APIRouter()

@router.get("/league/{id}")
def get_league(id: int):
    league = sorted(users, key=lambda x: x["quiz"]["solved_quiz"], reverse=True)
    #print(users)
    league_position = None
    for i in range(len(league)):
        if(league[i]["id"] == id):
            league_position = i
            break
    user_datas_for_league=[]
    if league_position is None:
        raise HTTPException(status_code=404, detail="User not found in league")
    pr = (league_position+1) / len(league) * 100
    i = 0
    cnt = 0
    while cnt<20:
        if i < 0 or i >= len(league):
            i += 1
            cnt += 1
            continue
        if league[i]["ranking"] == league[league_position]["ranking"]:
            i += 1
            continue
        i += 1
        cnt += 1
        league_data= {
        "all_user_id": league[i]["id"],
        "league_position": league_position+1,
        "pr": pr,
        "ranking": league [i]["ranking"],
        }
        user_datas_for_league.append(league_data)
    return user_datas_for_league






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

