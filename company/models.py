from datetime import datetime, timezone
import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean, ForeignKey

from core.database import Base

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String, primary_key=True, default= lambda : str(uuid.uuid4()))

    name: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default= lambda: datetime.now(timezone.utc))

