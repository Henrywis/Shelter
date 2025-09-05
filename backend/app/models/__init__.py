# Makes app.models a package and exposes Base for easy imports
from .base import Base
from .user import User
from .shelter import Shelter
from .capacity import CapacityLog
from .intake import IntakeRequest

__all__ = ["Base", "User", "Shelter", "CapacityLog", "IntakeRequest"]

