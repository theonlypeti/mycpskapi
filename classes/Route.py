from classes import Station


class Route(object):
    def __init__(self, cities: list[Station], meska: int, traintype: str | None, distance: int = None):
        # self.departure: datetime = departure
        # self.arrival: datetime = arrival
        self.stations: list[Station] = cities
        # self.origin = self.stations[0].name
        # self.destination = self.stations[-1].name
        self.delay: int = meska
        self.traintype: str | None = traintype
        self.distance: int = distance

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

    def __repr__(self):
        return f"{self.__class__}({self.departure},{self.arrival},{self.stations}, {self.delay}, {self.traintype}, {self.distance})"

    def __str__(self):
        return f"Route:\n{self.departure=}\n{self.arrival=}\n{self.delay=}\n{self.traintype=}\n{self.distance=}\nself.cities=" + '\n\t'.join((str(st) for st in self.stations))
