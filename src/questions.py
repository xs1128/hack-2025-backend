from fastapi import APIRouter
from custom_types import User
from shared_data import users

router = APIRouter()


@router.post("/quiz/answer")
def answer_quiz(user: User, question_id: int, answer: str):
    # Check if user exists
    if user not in users:
        return {"error": "User not found"}

    # Find the question by ID
    # question = q for q in user["quiz"]["questuions"] if q["id"] == question_id
    if not question:
        return {"error": "Question not found"}
        question = question[0]  # Get the first match
        # Check if the answer is correct
    if question["answer"] == answer:
        # Update user's quiz data
        user["quiz"]["current_streak"] += 1
        user["quiz"]["solved_quiz"] += 1
        return {"message": "Correct answer!"}
    else:
        user["quiz"]["current_streak"] = 0
        return {"message": "Interesting answer, but not correct!, try again!"}
