from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase, Employee, ContactMessage
from viewer.forms import EmployeeForm, OrderForm, TravelInfoForm, ContactMessageForm
from datetime import date, timedelta
from django.utils import timezone


class BaseTestCase(TestCase):
    def setUp(self):
        # Create Continent
        self.continent = Continent.objects.create(name="Europe")
        # Create Country
        self.country = Country.objects.create(name="Czech Republic", continent=self.continent)
        # Create City
        self.city = City.objects.create(name="Prague", country=self.country)
        # Create Hotel
        self.hotel = Hotel.objects.create(name="Hotel Prague", city=self.city)

        # Test user and employee
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.employee = Employee.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            role="Manager",
            email="john.doe@example.com",
            phone="123456789"
        )


class ContinentModelTest(BaseTestCase):
    def test_create_continent(self):
        self.assertEqual(self.continent.name, 'Europe')
        self.assertTrue(Continent.objects.exists())


class CountryModelTest(BaseTestCase):
    def test_create_country(self):
        self.assertEqual(self.country.name, 'Czech Republic')
        self.assertEqual(self.country.continent.name, 'Europe')


class CityModelTest(BaseTestCase):
    def test_create_city(self):
        self.assertEqual(self.city.name, 'Prague')
        self.assertEqual(self.city.country.name, 'Czech Republic')


class HotelModelTest(BaseTestCase):
    def test_create_hotel(self):
        self.assertEqual(self.hotel.name, 'Hotel Prague')
        self.assertEqual(self.hotel.city.name, 'Prague')


class CityModelTest(TestCase):
    def setUp(self):
        # Create necessary dependencies
        self.continent = Continent.objects.create(name="Europe")
        self.country = Country.objects.create(name="Czech Republic", continent=self.continent)
        self.city = City.objects.create(name="Prague", country=self.country)

    def test_create_city(self):
        self.assertEqual(self.city.name, "Prague")
        self.assertEqual(self.city.country.name, "Czech Republic")
        self.assertEqual(self.city.country.continent.name, "Europe")


class AirportModelTest(BaseTestCase):
    def test_create_airport(self):
        self.assertEqual(self.airport.name, 'Vaclav Havel Airport')
        self.assertEqual(self.airport.city.name, 'Prague')


class TravelInfoModelTest(BaseTestCase):
    def test_create_travel_info(self):
        travel_info = TravelInfo.objects.create(
            tour_name='Spring Holiday',
            departure_city=self.city,
            departure_airport=self.airport,
            destination_city=self.city,
            destination_airport=self.airport,
            departure_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=7),
            stay_duration=7,
            meal_type='BB',
            price_per_adult=5000,
            price_per_child=2500,
            adult_seats=50,
            child_seats=25,
            assigned_to=self.employee
        )
        travel_info.destination_hotels.set([self.hotel])

        self.assertEqual(travel_info.tour_name, 'Spring Holiday')
        self.assertEqual(travel_info.departure_city.name, 'Prague')
        self.assertEqual(travel_info.destination_hotels.first().name, 'Hotel Prague')
        self.assertEqual(travel_info.price_per_adult, 5000)


class TourPurchaseModelTest(BaseTestCase):
    def test_create_tour_purchase(self):
        travel_info = TravelInfo.objects.create(
            tour_name='Spring Holiday',
            departure_city=self.city,
            departure_airport=self.airport,
            destination_city=self.city,
            destination_airport=self.airport,
            departure_date=timezone.now().date(),
            return_date=timezone.now().date() + timedelta(days=7),
            stay_duration=7,
            meal_type='BB',
            price_per_adult=5000,
            price_per_child=2500,
            adult_seats=50,
            child_seats=25,
            assigned_to=self.employee
        )
        travel_info.destination_hotels.set([self.hotel])

        tour_purchase = TourPurchase.objects.create(
            travel_info=travel_info,
            adult_count=2,
            child_count=1,
        )
        self.assertEqual(tour_purchase.total_quantity, 3)
        self.assertEqual(tour_purchase.total_price, 12500)  # 2 adults + 1 child
        self.assertEqual(tour_purchase.adult_count, 2)
        self.assertEqual(tour_purchase.child_count, 1)


class FormsTestCase(BaseTestCase):
    def test_employee_form_valid(self):
        data = {
            'username': 'employeeuser',
            'password': 'securepassword',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'role': 'Senior',
            'email': 'jane.smith@example.com',
            'phone': '987654321',
            'assigned_trips': []
        }
        form = EmployeeForm(data)
        self.assertTrue(form.is_valid())

    def test_order_form_valid(self):
        data = {
            'adult_count': 2,
            'child_count': 1,
            'customer_name': 'Alice Johnson',
            'customer_email': 'alice.johnson@example.com',
            'customer_phone': '123456789',
            'customer_address': '123 Main Street',
            'special_requests': 'Vegetarian meals',
            'payment_method': 'Credit Card',
            'order_status': 'Pending',
        }
        form = OrderForm(data)
        self.assertTrue(form.is_valid())

    def test_travel_info_form_valid(self):
        uploaded_image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'tour_name': 'Best Tour',
            'departure_city': self.city.id,
            'destination_city': self.city.id,
            'departure_date': date.today(),
            'return_date': date.today(),
            'stay_duration': 7,
            'adult_seats': 50,
            'child_seats': 20,
            'price_per_adult': 100.0,
            'price_per_child': 50.0,
            'meal_type': 'Full Board',
            'assigned_to': self.employee.id,
            'description': 'An amazing tour!',
            'Hotel': self.hotel.id,
            'is_promoted': True,
        }
        form = TravelInfoForm(data, files={'image': uploaded_image})
        self.assertTrue(form.is_valid())

    def test_contact_message_form_valid(self):
        data = {
            'status': 'Pending',
            'assigned_to': self.employee.id,
            'comments': 'Please handle this message.',
        }
        form = ContactMessageForm(data)
        self.assertTrue(form.is_valid())
