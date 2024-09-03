from sqlalchemy import Integer, Column, String, Boolean

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)

    telegram_id = Column(Integer, nullable=False, unique=True)
    itmo_id = Column(Integer, unique=True, nullable=True)
    username = Column(String)
    is_admin = Column(Boolean, default=False)
    verified = Column(Boolean, default=False)
