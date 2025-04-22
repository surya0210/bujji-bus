from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.orm.registry import mapper_registry
import uuid

operator_table = Table(
   "operators", 
   mapper_registry.metadata,
   Column("id",String,primary_key=True,default=lambda :str(uuid.uuid4())),
   Column("name", String(100), nullable=False),
   Column("email", String(100), nullable=False, unique=True),
   Column("password_hash", String(255), nullable=False),
   Column("created_at", DateTime, default=datetime.now),
   Column("is_active", Boolean, default=True),
)