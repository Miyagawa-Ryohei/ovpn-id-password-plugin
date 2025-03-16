import dataclasses
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

class User(declarative_base()):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    salt= Column(String, nullable=False)
    administrator=Column(Boolean, default=False)
    last_access=Column(DateTime, nullable=True)
    created_at=Column(DateTime, default=datetime.now())
    disabled = Column(Boolean, default=False)
