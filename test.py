import unittest
from datetime import datetime, timedelta
from classes.RouteSpecs import RouteSpecs
from main import get_itinerary, find_stations, autocomplete_stations

itin_podh_ba = get_itinerary("Podhájska", "Bratislava hl.st.", datetime(2024, 1, 1, 17, 0))
itin_ba_wien = get_itinerary("Bratislava hl.st.", "Wien Hbf", datetime(2024, 1, 14, 6, 0))
itin_pozb_ba = get_itinerary("Pozba", "Bratislava hl.st.", datetime(2024, 1, 1, 17, 0))


class TestMain(unittest.TestCase):

    def test_get_itinerary_with_valid_input(self):
        self.assertIsNotNone(itin_podh_ba)

    def test_get_itinerary_without_depart_time(self):
        departure = "Podhájska"
        destination = "Bratislava hl.st."
        itinerary = get_itinerary(departure, destination)
        self.assertIsNotNone(itinerary)

    def test_find_stations_with_valid_input(self):
        name = "Podhajska"
        stations = find_stations(name)
        self.assertIn("Podhájska", stations)

        name = "wien " #TODO now this does not get found without a space because theres a city twith a shorter levenstein distance
        stations = find_stations(name)
        # print(stations)
        self.assertIn("Wien Hbf", stations)

    def test_autocomplete_stations_with_valid_input(self):
        name = "pod"
        stations = autocomplete_stations(name)
        # print(stations)
        self.assertIn("Podhájska", stations)

        name = "wien h"
        stations = autocomplete_stations(name)
        self.assertIn("Wien Hbf", stations)

    def test_itin_duration(self):
        print(itin_podh_ba.length)
        print(itin_podh_ba.pprint())
        self.assertTrue(timedelta(hours=2) > itin_podh_ba.length > timedelta(hours=1))
        self.assertTrue(itin_podh_ba.length < itin_pozb_ba.length)


class TestDunderMethods(unittest.TestCase):

    def test_itinerary_length_returns_correct_value(self):
        self.assertEqual(len(itin_pozb_ba), 3)
        self.assertEqual(len(itin_pozb_ba.routes), 3)

    def test_itinerary_eq_returns_true_for_same_routes(self):
        itinerary1 = itin_pozb_ba
        itinerary2 = get_itinerary("Pozba", "Bratislava hl.st.", datetime(2024, 1, 1, 17, 1))
        self.assertTrue(itinerary1 == itinerary2)

    def test_itinerary_eq_returns_false_for_different_routes(self):
        itinerary1 = itin_pozb_ba
        itinerary2 = get_itinerary("Pozba", "Bratislava hl.st.", datetime.now() + timedelta(hours=24))
        self.assertFalse(itinerary1 == itinerary2)


class TestRouteSpecs(unittest.TestCase):

    def test_contains_returns_true_for_existing_attribute(self):
        route_specs = RouteSpecs(["º"])
        route_specs.internet = True
        self.assertTrue('internet' in route_specs)

    def test_contains_returns_false_for_non_existing_attribute(self):
        route_specs = RouteSpecs(["r"])
        self.assertFalse('internet' in route_specs)

    def test_list_returns_all_attributes(self):
        route_specs = RouteSpecs(["º", "M"])
        self.assertEqual(route_specs.list(), ['internet', 'restaurant'])

    def test_specs(self):
        itin = itin_ba_wien
        # print(itin.routes[0].name)
        # print(itin.routes[0].specs.list())
        self.assertIsNotNone(itin)
        self.assertIsNotNone(itin.routes[0].specs)
        self.assertIsNotNone(itin.routes[0].specs.quiet_zone)


if __name__ == '__main__':
    unittest.main()

# from unittest.mock import patch, MagicMock
#
# class TestMain(unittest.TestCase):
#     @patch('main.get_itinerary')
#     def test_get_itinerary_with_valid_input(self, mock_get_itinerary):
#         # Arrange
#         mock_get_itinerary.return_value = MagicMock()  # Replace with a suitable mock return value
#
#         # Act
#         result = get_itinerary("Podhájska", "Bratislava hl.st.", datetime.now())
#
#         # Assert
#         self.assertIsNotNone(result)
#         mock_get_itinerary.assert_called_once_with("Podhájska", "Bratislava hl.st.", datetime.now())

# todolearnlol this is confusing and a little bit overcomplicated for my simple classes