from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import db_url


Base = declarative_base()

engine = create_engine(db_url, echo=True)
SessionFactory = sessionmaker(bind=engine, expire_on_commit=False)