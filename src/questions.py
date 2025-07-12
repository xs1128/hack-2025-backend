import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Assume these are defined in your other files
from custom_types import User, Question
from shared_data import users

# --- Pydantic Model for POST requests ---
class AnswerPayload(BaseModel):
    user_id: int
    question_id: int
    submitted_answer: str

# --- Router Setup ---
router = APIRouter()

# --- Load Questions Library Safely ---
script_directory = Path(__file__).parent
file_path = script_directory / "questions_library.json"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        questions_library: list[Question] = json.load(f)
except FileNotFoundError:
    print(f"ERROR: questions_library.json not found at {file_path}")
    questions_library = []


# --- Corrected Endpoints ---

@router.get("/quiz/daily-question")
def get_daily_question(user_id: int):
    """
    Gets the current daily question for a specific user.
    Pass the user's ID in the URL, e.g., /quiz/daily-question?user_id=1
    """
    # 1. Find the user in the list
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Get the user's current question ID
    current_question_id = user['quiz']['current_id']

    # 3. Find the corresponding question in the library
    question = next((q for q in questions_library if q['id'] == current_question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail=f"Question with ID {current_question_id} not found")

    # 4. Return the entire question object (statement and options)
    return {"statement": question["statement"], "options": question["options"]}


@router.post("/quiz/daily-question-answer")
def submit_quiz_answer(payload: AnswerPayload):
    """
    Submits a user's answer to a question.
    """
    # 1. Find the user and the question from the payload
    user = next((u for u in users if u['id'] == payload.user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    question = next((q for q in questions_library if q['id'] == payload.question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # 2. Check if the submitted answer is correct
    if question['answer'] == payload.submitted_answer:
        # 3. Update user's stats on correct answer
        user['quiz']['current_streak'] += 1
        user['quiz']['solved_quiz'] += 1
        user['quiz']['current_id'] += 1  # Move to the next question
        return {"message": "Correct answer!", "is_correct": True}
    else:
        user['quiz']['current_streak'] = 0  # Reset streak
        return {"message": "Incorrect answer. Try again!", "is_correct": False}