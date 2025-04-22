from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.orm.registry import mapper_registry
import uuid

bus_table = Table(
    "buses",
    mapper_registry.metadata,
    Column("id",String,primary_key=True,default=lambda :str(uuid.uuid4())),
    Column("operator_id", String, ForeignKey("operators.id"), nullable=False),
    Column("bus_number", String(50), nullable=False),
    Column("total_seats", Integer, nullable=False),
    Column("bus_type", String(50), nullable=False),
    Column("model", String(100), nullable=True),
    Column("has_wifi", Boolean, default=False),
    Column("has_toilet", Boolean, default=False),
    Column("has_ac", Boolean, default=False),
    Column("active", Boolean, default=True),
    Column("last_service_date", DateTime, default=datetime.now),
    Column("next_service_due", DateTime, default=datetime.now),
    Column("created_at", DateTime, default=datetime.now),
    Column("last_updated_at", DateTime, default=datetime.now),
)
