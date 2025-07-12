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
    print(f"[DEBUG] users: {users}")
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        print(f"[DEBUG] User with id {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")

    # 2. Get the user's current question ID
    current_question_id = user['quiz']['current_id']
    print(f"[DEBUG] current_question_id: {current_question_id}")

    # 3. Find the corresponding question in the library
    print(f"[DEBUG] questions_library: {questions_library}")
    question = next((q for q in questions_library if q['id'] == current_question_id), None)
    if not question:
        print(f"[DEBUG] Question with ID {current_question_id} not found in questions_library.")
        raise HTTPException(status_code=404, detail=f"Question with ID {current_question_id} not found")

    # 4. Return the entire question object (statement and options)
    print(f"[DEBUG] Returning question: {question}")
    return {"question_id": question["id"], "statement": question["statement"], "options": question["options"]}


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

    # Return 'correct answer' if the answer is correct, otherwise return the correct answer
    if question['answer'] == payload.submitted_answer:
        user['quiz']['current_id'] += 1  # Move to the next question
        return {"message": "correct answer"}
    else:
        return {"answer": question['answer']}