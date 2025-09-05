from sqlalchemy import Column, Integer, String, Float, Text
from .base import Base
from .mixins import TimestampMixin

class Shelter(TimestampMixin, Base):
    __tablename__ = "shelters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    geo_lat = Column(Float, nullable=False)
    geo_lng = Column(Float, nullable=False)
    phone = Column(String, nullable=True)
    policies = Column(Text, nullable=True)  # JSON-ish text
    hours = Column(String, nullable=True)   # e.g. "9am–9pm"
