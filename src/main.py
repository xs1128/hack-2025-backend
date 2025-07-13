from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users import router as users_router
from leagues import router as leagues_router
from emails import router as emails_router
from questions import router as questions_router
from streak import router as streak_router
from store import router as store_router

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(leagues_router)
app.include_router(emails_router)
app.include_router(questions_router)
app.include_router(streak_router)
app.include_router(store_router)
