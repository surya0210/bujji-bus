from sqlalchemy.orm import relationship
from app.orm.registry import mapper_registry

from app.entities.operator_entity import Operator
from app.entities.bus_entity import Bus
from app.entities.seat_entity import Seat
from app.entities.route_entity import Route
from app.entities.route_stop_entity import RouteStop
from app.entities.passengers import Passenger
from app.entities.booking import Booking

from app.orm.operator_table import operator_table
from app.orm.bus_table import bus_table
from app.orm.seat_table import seat_table
from app.orm.route_table import route_table
from app.orm.route_stop_table import route_stop_table
from app.orm.passenger_table import passenger_table
from app.orm.booking_table import booking_table

def start_mappers():
   mapper_registry.map_imperatively(
       Operator,
       operator_table,
       properties={
           "buses": relationship(Bus, backref="operator", cascade="all, delete-orphan"),
           "routes": relationship(Route, backref="operator", cascade="all, delete-orphan"),
       },
   )

   mapper_registry.map_imperatively(
       Bus,
       bus_table,
       properties={
           "seats": relationship(Seat, backref="bus", cascade="all, delete-orphan"),
       },
   )

   mapper_registry.map_imperatively(Seat, seat_table)

   mapper_registry.map_imperatively(
       Route,
       route_table,
       properties={
           "stops": relationship(
               RouteStop,
               backref="route",
               cascade="all, delete-orphan",
               order_by=route_stop_table.c.stop_order,
           )
       },
   )

   mapper_registry.map_imperatively(RouteStop, route_stop_table)

   mapper_registry.map_imperatively(
       Passenger,
       passenger_table,
   )

   mapper_registry.map_imperatively(
       Booking,
       booking_table,
       properties={
           "seat": relationship(Seat, backref="bookings"),
           "operator": relationship(Operator, backref="bookings"),
           "route": relationship(Route, backref="bookings"),
       },
   )