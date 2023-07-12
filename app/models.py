from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

from app.database import Base


class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    host = Column(String(50))

    def __init__(self, name=None, host=None):
        self.name = name
        self.host = host

    def __repr__(self):
        return f"<Server {self.name!r} {self.host}>"


class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True)
    server = Column(String(50))
    response_time = Column(Integer)
    timestamp = Column(DateTime(timezone=True))

    def __init__(self, server=None, response_time=None, timestamp=None):
        self.server = server
        self.response_time = response_time
        self.timestamp = timestamp
