from fastapi import APIRouter, Depends, HTTPException
from ..schemas import TaskCreate
from ..security.database import SessionLocal,get_db
from ..models import Task
from ..security import auth

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
def create_task(task : TaskCreate,db=Depends(get_db),current_user = Depends(auth.get_current_user)):      ## Task Create is our pydantic model
    new_task = Task(**task.model_dump(),user_id = current_user.id)                    ## This will create pydantic model to dict 
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task  

@router.get("/get-tasks")
def get_task(db=Depends(get_db),current_user = Depends(auth.get_current_user)):
    try:
        tasks = db.query(Task).filter(Task.user_id==current_user.id).all()
        return tasks
    except Exception as e:
        print(f"Error {e}")

@router.get("/get-tasks/{task_id}")
def get_task(task_id : int,db=Depends(get_db),current_user = Depends(auth.get_current_user)):
    tasks = db.query(Task).filter(Task.id==task_id).first()
    if not tasks:
        raise HTTPException(status_code= 404, detail="Task not found")
    if tasks.user_id != current_user.id:
        raise HTTPException(status_code= 404, detail="Forbidden")
    return tasks


### This Is Manually Updating ###
@router.put("/update-task/{id}")
def update_task(id:int,task:TaskCreate,db=Depends(get_db),current_user = Depends(auth.get_current_user)):
    tasks_exist = db.query(Task).filter(Task.id==id).first()
    if not tasks_exist:
        raise HTTPException(status_code=404,detail="Task not found")
    if tasks_exist.user_id != current_user.id:
        raise HTTPException(status_code= 403, detail="Forbidden")
    tasks_exist.title = task.title
    tasks_exist.description = task.description
    tasks_exist.completed = task.completed
    db.commit()
    db.refresh(tasks_exist)
    return tasks_exist

### This is Dynamic Updating ###
@router.put("/update-task-dynamically/{id}")
def update_task(id:int,task:TaskCreate,db=Depends(get_db),current_user = Depends(auth.get_current_user)):
    tasks_exist = db.query(Task).filter(Task.id==id).first()
    if not tasks_exist:
        raise HTTPException(status_code=404,detail="Task not found")
    if tasks_exist.user_id != current_user.id:
        raise HTTPException(status_code= 403, detail="Forbidden")
    
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
def delete_task(id:int,db=Depends(get_db),current_user = Depends(auth.get_current_user)):
    tasks_exist = db.query(Task).filter(Task.id==id).first()
    if not tasks_exist:
        raise HTTPException(status_code=404,detail="Task not found")
    if tasks_exist.user_id != current_user.id:
        raise HTTPException(status_code= 403, detail="Forbidden")
    db.delete(tasks_exist)
    db.commit()
    return {"message":"Task is deleted"}
    