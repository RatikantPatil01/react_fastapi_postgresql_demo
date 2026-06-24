from ..security.database import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)