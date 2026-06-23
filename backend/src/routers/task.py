from fastapi import APIRouter
from ..schemas import TaskCreate

router = APIRouter(prefix="/tasks",tags=['Tasks'])

@router.post("/create-task")
def create_task(task : TaskCreate):
    return {"message":"New task is created"}