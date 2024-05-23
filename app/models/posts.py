import datetime

from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from sqlalchemy import String, Boolean, UUID, text
from sqlalchemy.sql.sqltypes import TIMESTAMP

Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=text("now()"))
