from datetime import datetime, timezone
import uuid

from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    full_name: Mapped[str] = mapped_column(String, nullable=True)

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    role: Mapped[str] = mapped_column(String, nullable=False, default="member")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))