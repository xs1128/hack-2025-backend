from fastapi import FastAPI

from users import router as users_router
from leagues import router as leagues_router
from emails import router as emails_router
from questions import router as questions_router
from streak import router as streak_router


'''
from shared_data import users
for i in range(50):
    users.append({
        "id": i,
        "name": f"User {i}",
        "email": "jdfsl@gmail.com",
        "created_at": "2023-10-01T00:00:00",
        "quiz": {
            "current_id": 1,
            "last_played": "2023-10-01T00:00:00",
            "current_streak": 0,
            "solved_quiz": 0,
        },
        "store": {
            "coin": 0,
            "freeze": 0,
        },
        "ranking": i % 5 + 1,
        }
    )
'''

app = FastAPI()

app.include_router(users_router)
app.include_router(leagues_router)
app.include_router(emails_router)
app.include_router(questions_router)
app.include_router(streak_router)
