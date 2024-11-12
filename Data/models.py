from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass

class Moderators(Base):
    __tablename__ = 'users'

    pk: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50))

class Customer(Base):
    __tablename__ = 'customers'

    pk: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    code: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(String(60))
    number: Mapped[str] = mapped_column(String(20))
    bonuses: Mapped[int] = mapped_column(Integer)
