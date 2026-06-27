# We are importing Base from database.py.
# Base is the parent class that helps us create database tables.
from ..security.database import Base

# We are importing different column types from SQLAlchemy.
# These types tell the database what kind of data each column will store.
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


# We are creating a table called Task.
# This class represents a table inside our database.
class Task(Base):

    # The name of the table inside the database.
    # SQLAlchemy will create a table called "tasks".
    __tablename__ = "tasks"


    # id column:
    # Integer = whole numbers (1, 2, 3, ...)
    # primary_key=True means every task gets a unique ID.
    # index=True makes searching by ID faster.
    id = Column(Integer, primary_key=True, index=True)


    # title column:
    # String(255) means text up to 255 characters.
    # nullable=False means a title is required.
    # A task cannot be created without a title.
    title = Column(String(255), nullable=False)


    # description column:
    # Stores extra details about the task.
    # nullable is True by default, so it can be empty.
    description = Column(String(255))


    # completed column:
    # Boolean means only True or False.
    # default=False means every new task starts as incomplete.
    completed = Column(Boolean, default=False)

    # Here we are creating a column where we are using foregion key for user table id 
    user_id = Column(Integer,ForeignKey("users.id"))