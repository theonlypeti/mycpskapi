import json
from datetime import timedelta, datetime
from itertools import zip_longest
import tabulate
from classes.Route import Route
from classes.Station import Station


class Itinerary(object):
    """
    An itinerary is a list of routes.
    Methods:

    pprint():
        Pretty prints the itinerary in a table.
    __str__():
        Returns a JSON representation of the itinerary.

    :ivar routes: A list of Route objects that make up the itinerary.
    :ivar departure: The departure time from the first station of the first route.
    :ivar origin: The first station of the first route.
    :ivar destination: The last station of the last route.
    :ivar arrival: The arrival time at the last station of the last route.
    :ivar duration: The total time the itinerary takes.
    :ivar distance: The total distance of the itinerary. Measured in kilometers.
    :ivar warnings: A dict of warnings of each route in this itinerary.
    """

    def __init__(self, routes: list[Route]):
        self.routes: list[Route] = routes or []
        # self.departure: datetime | None = departure
        # self.arrival: datetime | None = arrival
        # self.length: timedelta = self.arrival - self.departure
        # logger.warning(self.routes[0].departure == self.departure)
        # logger.warning(self.routes[-1].arrival == self.arrival)

    @property
    def origin(self) -> Station:
        return self.routes[0].origin

    @property
    def destination(self) -> Station:
        return self.routes[-1].destination

    @property
    def departure(self) -> datetime:
        return self.routes[0].departure

    @property
    def arrival(self) -> datetime:
        return self.routes[-1].arrival

    @property
    def distance(self) -> int:
        return sum(route.distance for route in self.routes)

    @property
    def length(self) -> timedelta:
        return self.arrival - self.departure

    @property
    def duration(self) -> timedelta:
        return self.length #todo deprecate length??

    @property
    def warnings(self) -> dict[str, list[str]] | None:
        warns = {}
        for rt in self.routes:
            if rt.warnings:
                warns[rt.name] = rt.warnings
        return warns or None

    def __len__(self):
        return len(self.routes)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.routes}, {self.departure}, {self.arrival}, {self.distance}, {self.length})"

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o), indent=4)

    def __iter__(self):
        return iter(self.routes)

    def __eq__(self, other):
        return (self.routes == other.routes and
                self.departure == other.departure and
                self.arrival == other.arrival)

    def __hash__(self):
        return hash((tuple(self.routes), self.departure, self.arrival))

    def pprint(self):
        transposed_data = list(map(list, zip_longest(*[[str(st) for st in route.stations] for route in self.routes], fillvalue="")))
        print(tabulate.tabulate(transposed_data, headers=[f"{route.traintype}; delay: {route.delay}min; distance: {route.distance}km" for route in self.routes], tablefmt="fancy_grid"))
        print(f"{self.warnings=}")

