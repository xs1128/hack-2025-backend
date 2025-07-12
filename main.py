from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from typing import TypedDict
from datetime import datetime

app = FastAPI()


class QuizData(TypedDict):
    current_id: int  # current question ID, starts from 1
    last_played: datetime
    current_streak: int  #
    solved_quiz: int  # number of quizzes solve


class StoreData(TypedDict):
    coin: int  # user coin balance
    freeze: int  # defrost item count


class User(TypedDict):
    id: int
    name: str | None
    email: str
    created_at: datetime  # date when account created
    quiz: QuizData
    store: StoreData


class Question(TypedDict):
    id : int
    statement: str
    options: list[str] # choose
    answer: str


# Store all users
users: list[User] = []


@app.get("/")
def root():
    return {"message": "Hello, 菇得!"}


@app.post("/user/setup")
def register_user(id: str):
    # Register success, redirect to game page
    ...


# Simple authentication endpoint
@app.post("/user")
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


@app.get("/league/{user_id}")
def get_league(user:User):
    league=sorted(users, key=lambda x: x["quiz"]["solved_quiz"], reverse=True)
    league_position = next((index + 1 for index, u in enumerate(league) if u["id"] == user["id"]), None)
    if league_position is None:
        return {"error": "User not found in league"}
    pr=league_position / len(league) *100
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
        "warn": warn if 'warn' in locals() else False,
        "promote": promote if 'promote' in locals() else False,
    }


@app.post("/quiz/answer")
def answer_quiz(user: User, question_id: int, answer: str):
    # Check if user exists
    if user not in users:
        return {"error": "User not found"}

    # Find the question by ID
    # question = q for q in user["quiz"]["questuions"] if q["id"] == question_id
    if not question:
        return {"error": "Question not found"}
        question = question[0] #Get the first match
        # Check if the answer is correct
    if question["answer"] == answer:
        # Update user's quiz data
        user["quiz"]["current_streak"] += 1
        user["quiz"]["solved_quiz"] += 1
        return {"message": "Correct answer!"}
    else:
        user["quiz"]["current_streak"] = 0
        return {"message": "Interesting answer, but not correct!, try again!"}