from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey,Time,Float
from app.orm.registry import mapper_registry

route_stop_table = Table(
    "route_stops",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False),
    Column("stop_name", String(100), nullable=False),
    Column("stop_order", Integer, nullable=False),
    Column("arrival_time", Time, nullable=True),
    Column("departure_time", Time, nullable=True),
    Column("distance_from_start", Integer, default=0),
    Column("price",Float,default=0.0)
)