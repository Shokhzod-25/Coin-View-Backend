from sqlalchemy import Column, String, Integer

from ..database import Base

class User(Base):
    __tablename__ = "users"

    user_name = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)

    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(12), unique=True, nullable=False)

    api_key = Column(String(255))
    req_count = Column(Integer, default=0, nullable=True)

    hash_password = Column(String(255), nullable=False)
