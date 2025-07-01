
from fastapi import APIRouter

from utils.search import search_skills


router = APIRouter()

@router.post("/skills_search_engine")
def test_model_endpoint(position:str):

    result = search_skills(position)
    return {"result": result}