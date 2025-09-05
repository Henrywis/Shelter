from sqlalchemy import Column, Integer, String, Enum
from .base import Base
from .mixins import TimestampMixin

class UserRole:
    ADMIN = "admin"
    SHELTER = "shelter"
    PUBLIC = "public"

class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default=UserRole.PUBLIC, nullable=False)
    shelter_id = Column(Integer, nullable=True)  # FK in future
