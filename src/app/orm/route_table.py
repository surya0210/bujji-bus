from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from app.orm.registry import mapper_registry

route_table = Table(
    "routes",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("operator_id", String, ForeignKey("operators.id"), nullable=False),
    Column("bus_id", String, ForeignKey("buses.id"), nullable=False),
    Column("origin", String(100), nullable=False),
    Column("destination", String(100), nullable=False),
    Column("distance_km", Integer, nullable=False),
    Column("route_time", Integer, nullable=False),
    Column("is_active", Boolean, default=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)
