from fastapi import APIRouter
from fastapi import HTTPException
from custom_types import User
from shared_data import users

router = APIRouter()

@router.get("/league/{id}")
def get_league(id: int):
    print(users)
    league = sorted(users, key=lambda x: x["quiz"]["solved_quiz"], reverse=True)
    print(type(league))
    league_position = None
    for i in range(len(league)):
        if league[i]["id"] == id:
            league_position = i
            break
    if league_position is None:
        raise HTTPException(status_code=404, detail="User not found in league")
    
    user_datas_for_league=[]
    start_index = max(0, league_position - 10)
    end_index = min(len(league), start_index + 11)
    for i in range(start_index, end_index):
        print(league[i])
        if league[i]["ranking"] != league[league_position]["ranking"]:
            if end_index < len(league):
                end_index += 1
            continue
        current_position = i + 1
        pr= (current_position / len(league)) * 100
        league_data= {
        "all_user_id": league[i]["id"],
        "league_position": league_position+1,
        "pr": pr,
        "ranking": league[i]["ranking"],
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

