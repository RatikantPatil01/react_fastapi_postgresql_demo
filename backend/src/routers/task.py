from fastapi import APIRouter, Depends, HTTPException
from ..schemas import TaskCreate
from ..security.database import SessionLocal,get_db
from ..models import Task


router = APIRouter(prefix="/tasks",tags=['Tasks'])

### *** Without Dependency Injection ***
# @router.post("/create-task")
# def create_task(task : TaskCreate):      ## Task Create is our pydantic model
#     db = SessionLocal()
#     new_task = Task(**task.model_dump())
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
#     db.close()
#     return new_task        

### *** With Dependency Injection ***
@router.post("/create-task")
def create_task(task : TaskCreate,db=Depends(get_db)):      ## Task Create is our pydantic model
    new_task = Task(**task.model_dump())                    ## This will create pydantic model to dict 
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task  

@router.get("/get-tasks")
def get_task(db=Depends(get_db)):
    try:
        tasks = db.query(Task).all()
        return tasks
    except Exception as e:
        print(f"Error {e}")

@router.get("/get-tasks/{task_id}")
def get_task(task_id : int,db=Depends(get_db)):
    tasks = db.query(Task).filter(Task.id==task_id).first()
    if not tasks:
        raise HTTPException(status_code= 404, detail="Task not found")
    return tasks


### This Is Manually Updating ###
@router.put("/update-task-manually/{id}")
def update_task(id:int,task:TaskCreate,db=Depends(get_db)):
    tasks_exist = db.query(Task).filter(Task.id==id).first()
    if not tasks_exist:
        raise HTTPException(status_code=404,detail="Task not found")
    tasks_exist.title = task.title
    tasks_exist.description = task.description
    tasks_exist.completed = task.completed
    db.commit()
    db.refresh(tasks_exist)
    return tasks_exist

### This is Dynamic Updating ###
@router.put("/update-task-dynamically/{id}")
def update_task(id:int,task:TaskCreate,db=Depends(get_db)):
    tasks_exist = db.query(Task).filter(Task.id==id).first()
    if not tasks_exist:
        raise HTTPException(status_code=404,detail="Task not found")
    
        # Get all fields from the incoming request as a dictionary
        # Example:
        # {
        #     "title": "Learn FastAPI",
        #     "completed": True
        # }

    for key, value in task.model_dump().items():

    # Dynamically update the existing database object
    #
    # Equivalent to:
    # tasks_exist.title = "Learn FastAPI"
    # tasks_exist.completed = True
    #
    # Here:
    # key   = field name ("title", "completed")
    # value = new value ("Learn FastAPI", True)
        setattr(tasks_exist, key, value)

    db.commit()
    db.refresh(tasks_exist)
    return tasks_exist

@router.delete("/delete-task")
def delete_task(id:int,db=Depends(get_db)):
    tasks_exist = db.query(Task).filter(Task.id==id).first()
    if not tasks_exist:
        raise HTTPException(status_code=404,detail="Task not found")
    db.delete(tasks_exist)
    db.commit()
    return {"message":"Task is deleted"}
    