class RouteSpecs:
    """
        The RouteSpecs class represents the specifications or features of a route in a train journey.

        Each attribute of the RouteSpecs class corresponds to a specific feature that a route's rolling stock can have, such as internet access, power sockets, and whether it has a sleeper or couchette cars.
    """
    def __init__(self, strings: list[str]):
        # chars = '³W1z.[LºªV2©wR¯íM®rH½'
        self._unknowns = []
        for char in strings:  # TODO should i do case match? that would severely limit the requirements to 3.10+
            # if char not in chars:
            #     pass
            if char == "R":
                self.seat_reservation_possible = True
            elif char == "r":
                self.seat_reservation_required = True
            elif char == "M":
                self.restaurant = True
            elif char == "º":
                self.internet = True
            elif char == "³":
                self.power_socket = True
            elif char == "®":
                self.children = True
            elif char == "¯":
                self.luggage_paid = True
            elif char == "í":
                self.bicycle_forbidden = True
            elif char == "ª":
                self.bicycle_paid = True
            elif char == "L":
                self.bicycle = True
            elif char == "©":
                self.wheelchair = True
            elif char == "H":
                self.no_wheelchair = True  # there is seating for wheelchair users but no ramp or elevator
            elif char == "z":
                self.replacement_bus = True
            elif char == "1.2.":
                self.first_class = True
            elif char == "2.":
                self.second_class_only = True
            elif char == "V":
                self.sleeper = True
            elif char == "W":
                self.couchette = True
            elif char == "[":
                self.car_transport = True
            elif char == "w":
                self.direct_carriage = True  # priamy vozeň, honestly idk
            elif char == "½":
                self.quiet_zone = True
            elif char == "kino":
                self.children_cinema = True

            else:
                self._unknowns.append(char)
        if self._unknowns:
            print(f"Unknown characters: {self._unknowns}")

    def __contains__(self, item):
        return getattr(self, item, False)

    def list(self):
        return [att for att in dir(self) if not att.startswith("_") and getattr(self, att) and not callable(getattr(self, att))]

    def __iter__(self):
        return iter(self.list())

    def __str__(self):
        return str(self.list())
