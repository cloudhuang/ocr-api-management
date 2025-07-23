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
    api_code = Column(String(64), nullable=False, unique=True, index=True, doc="API 代码，用于唯一标识API")
    name = Column(String(128), nullable=False, doc="API 名称")
    description = Column(String(256), nullable=True, doc="API 描述")
    definition = Column(Text, nullable=False, doc="API 定义的 JSON 字符串")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, doc="创建时间")