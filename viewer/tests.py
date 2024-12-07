from django.test import TestCase
from .models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase
from django.utils import timezone
from datetime import timedelta


class ContinentModelTest(TestCase):
    def test_create_continent(self):
        continent = Continent.objects.create(name='Europe')
        self.assertEqual(continent.name, 'Europe')
        self.assertTrue(Continent.objects.exists())


class CountryModelTest(TestCase):
    def test_create_country(self):
        continent = Continent.objects.create(name='Europe')
        country = Country.objects.create(name='Czech Republic', continent=continent)
        self.assertEqual(country.name, 'Czech Republic')
        self.assertEqual(country.continent.name, 'Europe')


class CityModelTest(TestCase):
    def test_create_city(self):
        continent = Continent.objects.create(name='Europe')
        country = Country.objects.create(name='Czech Republic', continent=continent)
        city = City.objects.create(name='Prague', Country=country)
        self.assertEqual(city.name, 'Prague')
        self.assertEqual(city.Country.name, 'Czech Republic')


class HotelModelTest(TestCase):
    def test_create_hotel(self):
        continent = Continent.objects.create(name='Europe')
        country = Country.objects.create(name='Czech Republic', continent=continent)
        city = City.objects.create(name='Prague', Country=country)
        hotel = Hotel.objects.create(name='Hotel Prague', City=city)
        self.assertEqual(hotel.name, 'Hotel Prague')
        self.assertEqual(hotel.City.name, 'Prague')


class AirportModelTest(TestCase):
    def test_create_airport(self):
        continent = Continent.objects.create(name='Europe')
        country = Country.objects.create(name='Czech Republic', continent=continent)
        city = City.objects.create(name='Prague', Country=country)
        airport = Airport.objects.create(name='Vaclav Havel Airport', City=city)
        self.assertEqual(airport.name, 'Vaclav Havel Airport')
        self.assertEqual(airport.City.name, 'Prague')


class TravelInfoModelTest(TestCase):
    def test_create_travel_info(self):
        continent = Continent.objects.create(name='Europe')
        country = Country.objects.create(name='Czech Republic', continent=continent)
        city = City.objects.create(name='Prague', Country=country)
        hotel = Hotel.objects.create(name='Hotel Prague', City=city)
        airport = Airport.objects.create(name='Vaclav Havel Airport', City=city)
        travel_info = TravelInfo.objects.create(
            tour_name='Spring Holiday',
            departure_city=city,
            departure_airport=airport,
            destination_city=city,
            destination_hotel=hotel,
            destination_airport=airport,
            departure_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=7),
            stay_duration=7,
            meal_type='BB',
            price_per_adult=5000,
            price_per_child=2500,
            adult_seats=50,
            child_seats=25,
        )
        self.assertEqual(travel_info.tour_name, 'Spring Holiday')
        self.assertEqual(travel_info.departure_city.name, 'Prague')
        self.assertEqual(travel_info.destination_hotel.name, 'Hotel Prague')
        self.assertEqual(travel_info.price_per_adult, 5000)


class TourPurchaseModelTest(TestCase):
    def test_create_tour_purchase(self):
        continent = Continent.objects.create(name='Europe')
        country = Country.objects.create(name='Czech Republic', continent=continent)
        city = City.objects.create(name='Prague', Country=country)
        hotel = Hotel.objects.create(name='Hotel Prague', City=city)
        airport = Airport.objects.create(name='Vaclav Havel Airport', City=city)
        travel_info = TravelInfo.objects.create(
            tour_name='Spring Holiday',
            departure_city=city,
            departure_airport=airport,
            destination_city=city,
            destination_hotel=hotel,
            destination_airport=airport,
            departure_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=7),
            stay_duration=7,
            meal_type='BB',
            price_per_adult=5000,
            price_per_child=2500,
            adult_seats=50,
            child_seats=25,
        )
        tour_purchase = TourPurchase.objects.create(
            travel_info=travel_info,
            adult_count=2,
            child_count=1,
        )
        self.assertEqual(tour_purchase.total_quantity, 3)
        self.assertEqual(tour_purchase.total_price, 12500)  # 2 adults + 1 child
        self.assertEqual(tour_purchase.adult_count, 2)
        self.assertEqual(tour_purchase.child_count, 1)
        self.assertTrue(tour_purchase.created_at)
        self.assertTrue(tour_purchase.updated_at)