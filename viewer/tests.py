from unittest import TestCase

from viewer.models import Continent, Country, City, Airport, Hotel, TravelInfo


class TravelInfoModelTest(TestCase):
    def setUp(self):
        # Create necessary dependencies for the TravelInfo model
        self.continent = Continent.objects.create(name="Europe")
        self.country = Country.objects.create(
            name="Czech Republic",
            continent=self.continent,
            International_code=420
        )
        self.city = City.objects.create(
            name="Prague",
            Country=self.country,
            International_code=123
        )
        self.airport = Airport.objects.create(
            name="Václav Havel Airport",
            City=self.city
        )
        self.hotel = Hotel.objects.create(
            name="Grand Hotel",
            Stars=5,
            Description="Luxury hotel in Prague.",
            City=self.city
        )

    def test_create_travel_info(self):
        # Create a TravelInfo object
        travel_info = TravelInfo.objects.create(
            tour_name="Amazing Prague Tour",
            departure_city=self.city,
            departure_airport=self.airport,
            destination_city=self.city,
            destination_hotel=self.hotel,
            departure_date="2024-12-20",
            return_date="2024-12-27",
            stay_duration=7,
            meal_type="BB",
            price_per_adult=15000.00,
            price_per_child=7500.00,
            is_promoted=True,
            adult_seats=20,
            child_seats=10,
        )

        # Assertions to verify the TravelInfo object
        self.assertEqual(travel_info.tour_name, "Amazing Prague Tour")
        self.assertEqual(travel_info.departure_city, self.city)
        self.assertEqual(travel_info.destination_hotel, self.hotel)
        self.assertEqual(travel_info.stay_duration, 7)
        self.assertEqual(travel_info.meal_type, "BB")
        self.assertTrue(travel_info.is_promoted)
        self.assertEqual(travel_info.adult_seats, 20)
        self.assertEqual(travel_info.child_seats, 10)

    def test_str_representation(self):
        # Create another TravelInfo object
        travel_info = TravelInfo.objects.create(
            tour_name="Quick Weekend Getaway",
            departure_city=self.city,
            destination_hotel=self.hotel,
            departure_date="2024-12-20",
            return_date="2024-12-22",
            stay_duration=2,
            meal_type="HB",
            price_per_adult=5000.00,
            price_per_child=2500.00,
            is_promoted=False,
            adult_seats=10,
            child_seats=5,
        )

        # Assert the string representation
        expected_str = "Prague -> Prague (2024-12-20 - 2024-12-22)"
        self.assertEqual(str(travel_info), expected_str)
