from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, MappedColumn
import os
from sqlalchemy import String, DateTime, Integer, func
from sqlalchemy.exc import IntegrityError
import datetime
import atexit

POSTGRES_USER = os.environ.get("POSTGRES_USER", "web_app")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "1234")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "app_db")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    @property
    def id_dict(self):
        return {"id": self.id}
    
class Announcement(Base):
    __tablename__ = "announcements"
    
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    title: MappedColumn[str] = mapped_column(String, unique=True)
    discription: MappedColumn[str] = mapped_column(String)
    registretion_time: MappedColumn[datetime.datetime] = mapped_column(
        DateTime,
        server_default = func.now()
    )
    owner: MappedColumn[str] = mapped_column(String)
    
    @property
    def dict(self):
        return {
            "id":self.id,
            "title": self.title,
            "discription": self.discription,
            "registration_time": self.registretion_time.timestamp(),
            "owner": self.owner
        }
    
Base.metadata.create_all(engine)
atexit.register(engine.dispose)