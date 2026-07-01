# We are importing FastAPI.
# FastAPI helps us create APIs (web services) using Python.
from fastapi import FastAPI


# We are importing our task router.
# The router contains all task-related API endpoints
# such as create task, get task, update task, and delete task.
from .routers import task,user


# We are importing Base and engine from database.py.
# Base knows about all our database tables.
# Engine is the connection between our app and the database.
from src.security.database import Base, engine


# We are importing the Task model.
# This makes sure FastAPI knows about the Task table.
from .models import Task
from .models.user import User
from fastapi.middleware.cors import CORSMiddleware


# Creating our FastAPI application.
# Think of this as starting our backend server.
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# This command creates all tables in the database.
# SQLAlchemy checks all models that inherit from Base.
# If a table does not exist, it creates it automatically.
Base.metadata.create_all(bind=engine)


# Creating a GET API endpoint.
# When someone visits the root URL "/",
# this function will run.
@app.get("/")
def root():

    # Returning a simple JSON response.
    return {
        "Message": "Backend Is Running"
    }


# Adding all task-related routes to the application.
# This tells FastAPI:
# "Include all APIs written inside task.py router."
app.include_router(task.router)

app.include_router(user.router)