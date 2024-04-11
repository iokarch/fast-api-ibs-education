from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, )
    name: Mapped[str]
    age: Mapped[int]
    adult: Mapped[bool] = mapped_column(default=False)
    message: Mapped[str] = mapped_column(nullable=True)