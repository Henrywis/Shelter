from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .base import Base
from .mixins import TimestampMixin

class IntakeRequest(TimestampMixin, Base):
    __tablename__ = "intake_requests"

    id = Column(Integer, primary_key=True, index=True)
    shelter_id = Column(Integer, ForeignKey("shelters.id"), nullable=False)
    name = Column(String, nullable=True)  # optional name
    reason = Column(String, nullable=True) 
    eta = Column(DateTime, nullable=True)    # text for ETA
    status = Column(String, default="pending", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        # SQLite treats CHECK as advisory; Postgres will enforce strictly.
        CheckConstraint(
            "status in ('pending','fulfilled','cancelled')",
            name="ck_intake_status"
        ),
    )

    shelter = relationship("Shelter", back_populates="intakes")
