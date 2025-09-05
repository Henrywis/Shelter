from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base
from .mixins import TimestampMixin

class IntakeRequest(TimestampMixin, Base):
    __tablename__ = "intake_requests"

    id = Column(Integer, primary_key=True, index=True)
    shelter_id = Column(Integer, ForeignKey("shelters.id"), nullable=False)
    name = Column(String, nullable=True)  # optional name
    eta = Column(String, nullable=True)   # text for ETA
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    shelter = relationship("Shelter", backref="intake_requests")
