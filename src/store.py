from shared_data import users
from fastapi import APIRouter, HTTPException

router = APIRouter()

# Price mapping
price_mapping = {
    "freeze": 15,
}


# Store site
@router.get("/store/{id}")
def get_resource(id: int):
    try:
        # Encapsulation later
        return users[id]["store"]
    except IndexError:
        raise HTTPException(status_code=400, detail="User not found")


@router.post("/store/buy/{id}")
def buy(id: int):
    # Check if enough money
    try:
        if users[id]["store"]["coin"] < price_mapping["freeze"]:
            raise HTTPException(status_code=400, detail="Not enough coins!")
    except IndexError:
        raise HTTPException(status_code=400, detail="User not found")
    users[id]["store"]["coin"] -= price_mapping["freeze"]
    users[id]["store"]["freeze"] += 1

    return {"user": users[id]}
