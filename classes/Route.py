from classes import Station
from classes.RouteSpecs import RouteSpecs


class Route(object):
    """
    A route is a list of stations with a departure and arrival time.

    :ivar departure: The departure time from the first station of the route.
    :ivar arrival: The arrival time at the last station in the route.
    :ivar origin: The first station of the route.
    :ivar destination: The last station of the route.
    :ivar stations: A list of Station objects that make up the route.
    :ivar delay: The current delay of the route's train.
    :ivar traintype: The type of the train.
    :ivar distance: The distance of the route in kilometers.
    :ivar warnings: A list of warnings of the current route.
    :ivar remarks: A list of informative remarks of the route.
    :ivar specs: A RouteSpecs object that holds all the attributes and info about the route's train.
    """
    def __init__(self, cities: list[Station], meska: int, traintype: str | None, distance: int = None, warnings=None, remarks=None, specs=None):
        # self.departure: datetime = departure
        # self.arrival: datetime = arrival
        self.stations: list[Station] = cities
        # self.origin = self.stations[0].name
        # self.destination = self.stations[-1].name
        self.delay: int = meska
        self.traintype: str | None = traintype
        self.distance: int | None = distance  # in km
        self.warnings: list[str] | None = warnings
        self.remarks: list[str] | None = remarks
        self.specs: RouteSpecs = specs

    @property
    def departure(self):
        return self.stations[0].departure

    @property
    def arrival(self):
        return self.stations[-1].arrival

    @property
    def origin(self):
        return self.stations[0]

    @property
    def destination(self):
        return self.stations[-1]

    @property
    def name(self):
        return f"{self.origin.name} -> {self.destination.name} at {str(self.departure)} by {self.traintype}"

    def __repr__(self):
        return f"{self.__class__}({self.departure}, {self.arrival}, {self.stations}, {self.delay}, {self.traintype}, {self.distance})"

    def __str__(self):
        return f"Route:\n{self.departure=}\n{self.arrival=}\n{self.delay=}\n{self.traintype=}\n{self.distance=}\nself.cities=" + '\n\t'.join((str(st) for st in self.stations))

    def __iter__(self):
        return iter(self.stations)

    def __eq__(self, other):
        if not isinstance(other, Route):
            raise TypeError(f"Cannot compare Route with {other.__class__}")
        return (self.stations == other.stations and
                self.departure == other.departure and
                self.arrival == other.arrival and
                self.delay == other.delay)

    def __hash__(self):
        return hash((tuple(self.stations), self.departure, self.arrival, self.delay))
