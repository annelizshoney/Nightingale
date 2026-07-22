from datetime import datetime

from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class Elder(Base):

    __tablename__ = "elders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    full_name: Mapped[str] = mapped_column(String(150))

    gender: Mapped[str] = mapped_column(String(20))

    phone: Mapped[str] = mapped_column(String(20))

    blood_group: Mapped[str] = mapped_column(String(5))

    date_of_birth: Mapped[Date]

    emergency_contact: Mapped[str] = mapped_column(String(20))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )