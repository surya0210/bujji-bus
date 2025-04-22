from sqlalchemy import Table, Column, Integer, String, DateTime
from datetime import datetime
from app.orm.registry import mapper_registry

passenger_table = Table(
    "passengers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("age", Integer, nullable=False),
    Column("gender",String(10),nullable=False)
    # Column("password_hash", String(255), nullable=False),
    # Column("phone_number", String(20), nullable=False),
    # Column("created_at", DateTime, default=datetime.now(), nullable=False),
    # Column("last_login_time", DateTime, default=datetime.now(), nullable=False),
)
