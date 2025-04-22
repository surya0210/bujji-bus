from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey,Boolean,Date,Float
from datetime import datetime
from app.orm.registry import mapper_registry


booking_table = Table(
    "bookings",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("pnr", String(20), nullable=False),
    Column("passenger_id", Integer, ForeignKey("passengers.id"), nullable=False),
    Column("operator_id", String, ForeignKey("operators.id"), nullable=False),
    Column("route_id", Integer, ForeignKey("routes.id"), nullable=False),
    Column("seat_id", String, ForeignKey("seats.id"), nullable=False),
    Column("origin",String,nullable=False),
    Column("destination",String,nullable=False),
    Column("start_stop_order", Integer, nullable=False),
    Column("end_stop_order", Integer, nullable=False),
    Column("travel_date", Date, nullable=False),
    Column("amount",Float,nullable=False),
    Column("booking_time", DateTime, default=datetime.now),
    Column("status", Boolean, default=False),
    Column("is_cancelled", Boolean, default=False),
    Column("cancelled_reason", String(255), default="", nullable=True),
)