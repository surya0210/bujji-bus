"""
File: run_server.py
Date: 16 April 2025
Company: Annalect
Primary Authors: Pasumarthi Surya Narayana
"""

from fastapi import FastAPI

# from app.middlewares.store_request_logs import StoreRequestLogs
from app.orm.mapper import start_mappers
from app.routes.bus_route import bus_router
from app.routes.operator_route import operator_router
from app.routes.seat_route import seat_router
from app.routes.bus_map_route import route_router
from app.routes.route_stop_route import route_stop_router
from app.routes.search_route import search_router
from app.routes.booking_route import booking_router

bujji_bus_app = FastAPI(
    title="Bujji-Bus",
    summary="This is Bujji-bus (demo) app which enables "
    "operators to signup and provide service to the users and then they will be able to book it and cancel for free(just for now)",
   version="0.1",
   docs_url="/bujji-app-api",
   redoc_url="/bujji-app-api-redoc"
)

start_mappers()

bujji_bus_app.include_router(operator_router)
bujji_bus_app.include_router(bus_router)
bujji_bus_app.include_router(seat_router)
bujji_bus_app.include_router(route_router)
bujji_bus_app.include_router(route_stop_router)
bujji_bus_app.include_router(search_router)
bujji_bus_app.include_router(booking_router)
# bujji_bus_app.add_middleware(StoreRequestLogs)
