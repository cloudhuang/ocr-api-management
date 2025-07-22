from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ApiDefinition(Base):
    """
    ORM model for storing API definitions.
    """
    __tablename__ = 'api_definitions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False, unique=True, doc="API 名称")
    description = Column(String(256), nullable=True, doc="API 描述")
    definition = Column(Text, nullable=False, doc="API 定义的 JSON 字符串")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, doc="创建时间") 