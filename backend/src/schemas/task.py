from pydantic import BaseModel

class TaskCreate(BaseModel):
    title : str = None
    description : str = None
    completed: bool = False
    