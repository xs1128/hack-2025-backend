from typing import TypedDict
from datetime import datetime


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
    id: int
    statement: str
    options: list[str]  # choose
    answer: str
