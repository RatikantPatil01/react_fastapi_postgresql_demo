from fastapi import FastAPI
from .routers import task

app = FastAPI()

@app.get("/")
def root():
    return{"Message":"Backend Is Running"}

app.include_router(task.router)