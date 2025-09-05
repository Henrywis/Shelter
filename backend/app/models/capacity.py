from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base
from .mixins import TimestampMixin

class CapacityLog(TimestampMixin, Base):
    __tablename__ = "capacity_logs"

    id = Column(Integer, primary_key=True, index=True)
    shelter_id = Column(Integer, ForeignKey("shelters.id"), nullable=False)
    beds_total = Column(Integer, nullable=False)
    beds_available = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"))

    shelter = relationship("Shelter", backref="capacity_logs")
