# We are taking a tool called create_engine from SQLAlchemy.
# This tool helps Python talk to our database.
from sqlalchemy import create_engine

# We are importing our configuration file.
# The configuration file stores important settings,
# like the database username, password, and database URL.
from src.security import config

# sessionmaker helps create database sessions.
# declarative_base helps us create database tables using Python classes.
from sqlalchemy.orm import sessionmaker, declarative_base


# create_engine() creates a connection between our application
# and the database using the URL stored in config.
# Think of it as building a road from our app to the database.
engine = create_engine(config.settings.database_url)


# SessionLocal is a factory that creates database sessions.
# A session is like opening a conversation with the database.
# We use it whenever we want to add, update, delete,
# or read data from the database.
SessionLocal = sessionmaker(

    # autocommit=False means changes are NOT saved automatically.
    # We must manually say "commit" when we want to save changes.
    autocommit=False,

    # autoflush=False means data is not automatically sent
    # to the database while we are still working with it.
    autoflush=False,

    # bind=engine tells SessionLocal which database connection to use.
    bind=engine
)


# Base is the parent class for all database models.
# Whenever we create a table (User, Product, Customer, etc.),
# it will inherit from Base.
# Think of Base as the blueprint from which all tables are created.
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
       db.close()