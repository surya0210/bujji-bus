from app.repositories.operator_repo import OperatorRepository
from app.repositories.bus_repo import BusRepository
from app.repositories.seat_repo import SeatRepository
from app.repositories.route_repo import RouteRepository
from app.repositories.route_stop_repo import RouteStopRepository
from app.repositories.passenger_repo import PassengerRepository
from app.repositories.booking_repo import BookingRepository
from app.common.session_maker import get_session



class UnitOfWork:

    def __init__(self,session):

        self.session = session

        self.operators = OperatorRepository(self.session)

        self.buses = BusRepository(self.session)

        self.seats = SeatRepository(self.session)

        self.routes = RouteRepository(self.session)

        self.route_stops = RouteStopRepository(self.session)

        self.passengers = PassengerRepository(self.session)

        self.bookings = BookingRepository(self.session)

    def commit(self):
        self.session.commit()

    def rollback(self):

        self.session.rollback()

    def __enter__(self):

        return self

    def __exit__(self, *args):

        if args[0]:

            self.rollback()

        else:

            self.commit()

        self.session.close()
