from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey,String,DateTime
from app.orm.registry import mapper_registry
import uuid
from datetime import datetime

seat_table = Table(
   "seats",
   mapper_registry.metadata,
   Column("id",String,primary_key=True,default=lambda :str(uuid.uuid4())),
   Column("bus_id", String, ForeignKey("buses.id",ondelete="CASCADE"), nullable=False),
   Column("seat_number", Integer, nullable=False),
   Column("window", Boolean, default=False),
   Column("has_charging_port", Boolean, default=False),
   Column("is_reclinable", Boolean, default=False),
   Column("is_active", Boolean, default=True),
   Column("row_number", Integer, nullable=False),
   Column("created_at", DateTime, default=datetime.now),
)