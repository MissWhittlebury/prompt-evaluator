from typing import Any
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Text, UniqueConstraint, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from pydantic import BaseModel


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO: Make this a DB trigger
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)

    traces: Mapped[list["Trace"]] = relationship(back_populates="user")


# TODO: Eventually we can structure this data and make this a sqlalchemy model
class TraceMetadata(BaseModel):
    use_case: str
    resource_id: str
    workflow_step: str
    model_version: str
    prompt_version: str


class Trace(Base):
    __tablename__ = "trace"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    generation: Mapped[str] = mapped_column(Text, nullable=False)
    ai_model_config_id: Mapped[int] = mapped_column(ForeignKey("ai_model_config.id"))
    _metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, name="metadata")

    user: Mapped[User] = relationship(back_populates="traces")
    ai_model_config: Mapped["AIModelConfig"] = relationship(back_populates="traces")

    @property
    def trace_metadata(self) -> TraceMetadata:
        return TraceMetadata(**self._metadata)

    @trace_metadata.setter
    def trace_metadata(self, value: dict[str, Any]) -> None:
        trace_metadata = TraceMetadata.model_validate(value)
        self._metadata = trace_metadata.model_dump()


class AIModelConfig(Base):
    __tablename__ = "ai_model_config"
    __table_args__ = (
        UniqueConstraint("name", "temperature", name="unique_name_temperature"),
    )

    name: Mapped[str]
    temperature: Mapped[float]

    traces: Mapped[list[Trace]] = relationship(back_populates="ai_model_config")
