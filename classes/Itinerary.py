import json
from datetime import timedelta, datetime
from itertools import zip_longest
import tabulate
from classes import Route
from classes.Station import Station


class Itinerary(object):
    def __init__(self, routes: list["Route"]):
        self.routes: list["Route"] = routes or []
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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.routes}, {self.departure}, {self.arrival}, {self.distance}, {self.length})"

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o), indent=4)

    def pprint(self):
    # Transpose the data
        transposed_data = list(map(list, zip_longest(*[[str(st) for st in route.stations] for route in self.routes], fillvalue="")))
        print(tabulate.tabulate(transposed_data, headers=[f"{route.traintype}; delay: {route.delay}min; distance: {route.distance}km" for route in self.routes], tablefmt="fancy_grid"))

