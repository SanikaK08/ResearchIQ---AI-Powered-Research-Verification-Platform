from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import Text, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Research(Base):

    __tablename__ = "research"

    research_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    query: Mapped[str] = mapped_column(
        String(500)
    )

    report: Mapped[str] = mapped_column(
        Text
    )

    verification: Mapped[str] = mapped_column(
        Text
    )

    sources: Mapped[list["ResearchSource"]] = relationship(
    back_populates="research",
    cascade="all, delete-orphan"
    )

    status: Mapped[str] = mapped_column(
    String(30),
    default="pending"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

class ResearchSource(Base):

    __tablename__ = "research_sources"

    source_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    research_id: Mapped[int] = mapped_column(
        ForeignKey("research.research_id")
    )

    title: Mapped[str] = mapped_column(
        String(500)
    )

    url: Mapped[str] = mapped_column(
        String(1000)
    )

    research: Mapped["Research"] = relationship(
        back_populates="sources"
    )