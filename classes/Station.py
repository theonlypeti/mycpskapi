from datetime import timedelta, datetime
from bs4.element import Tag


class Station(object):
    def __init__(self, name: str, arrival: datetime, departure: datetime):
        self.name: str = name
        self.arrival: datetime = arrival
        self.departure: datetime = departure

    def __repr__(self):
        return f"{self.__class__}({self.name},{self.arrival},{self.departure})"

    def __str__(self):
        return f"Station:\n{self.name=}\n{self.arrival=}\n{self.departure=}"

    @classmethod
    def from_soup(cls, elem: Tag, date: datetime):
        name = elem.find("strong", attrs={"class": "name"}).text.strip()
        arrival_time = elem.find("span", attrs={"class": "arrival"}).text.strip()
        departure_time = elem.find("span", attrs={"class": "departure"}).text.strip()

        # Combine date and time before parsing
        if arrival_time:
            arrival = date.replace(hour=int(arrival_time.split(":")[0]), minute=int(arrival_time.split(":")[1]))
        else:
            arrival = None
        if departure_time:
            departure = date.replace(hour=int(departure_time.split(":")[0]), minute=int(departure_time.split(":")[1]))
        else:
            departure = None

            # Check if time has rolled over midnight
        if departure and arrival and departure < arrival:
            departure += timedelta(days=1)

        return Station(name, arrival, departure)


