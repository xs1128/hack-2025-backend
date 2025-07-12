from fastapi import APIRouter

router = APIRouter()


@router.get("/sample")
def sample_endpoint():
    pass
