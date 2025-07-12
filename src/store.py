from shared_data import users
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Price mapping
price_mapping = {
    "freeze": 15,
}


# Store site
@router.get("/store/{id}")
def get_store(id: int):
    # Encapsulation later
    return users[id]["store"]


@router.post("/store/{id}")
def post_store(id: int):
    # Check if enough money
    try:
        if users[id]["store"]["coin"] < price_mapping["freeze"]:
            return HTTPException(status_code=400, detail="Not enough coins!")
    except IndexError as err:
        raise HTTPException(status_code=400, detail=f"{err}")
    users[id]["store"]["coin"] -= price_mapping["freeze"]
    users[id]["store"]["freeze"] += 1

    return {"user": users[id]}
