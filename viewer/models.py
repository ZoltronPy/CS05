from django.core.exceptions import ValidationError
from django.forms import forms
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now

import logging

logger = logging.getLogger(__name__)

from django.db import models
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, IntegerField, DateField


#'vytvoření kontinetu'
class Continent(Model):
    name = CharField(max_length=32,
                     unique=True, null=False,
                     blank=False, db_index=True,
                     verbose_name="NAME")

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'Continent(name={self.name})'

    def __str__(self):
        return self.name


#vytvoření Států
class Country(Model):
    name = CharField(max_length=50, blank=False, unique=True, null=False)
    continent = ForeignKey(Continent, on_delete=CASCADE, related_name="countries")
    international_code = CharField(max_length=10, blank=True, unique=True, null=True,
                                   verbose_name="International Code")

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Countries'

    def __repr__(self):
        return f'Country(name={self.name}, continent={self.continent.name})'

    def __str__(self):
        return f"{self.name} ({self.continent.name})"


# Město
class City(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    country = ForeignKey(Country, on_delete=CASCADE, null=False, blank=False,
                         related_name="cities")
    description = TextField(null=True, blank=True)

    @property
    def continent_code(self):
        if self.country and self.country.continent:
            return self.country.continent.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cities'

    def __repr__(self):
        return (f'City(name={self.name},'
                f' country={self.country.name}, continent={self.continent_code})')

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Hotel(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    Stars = IntegerField(null=True, blank=True, default=3)
    Description = TextField(null=True, blank=True)

    City = ForeignKey(City, on_delete=CASCADE, related_name="city_hotels",
                      null=False, blank=False, )
    image = models.ImageField(upload_to="hotels", blank=True, null=True, verbose_name="Hotel Image")

    def clean(self):
        if not self.City:
            raise ValidationError("Hotel musí mít přiřazené město.")

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Hotels'

    def __repr__(self):
        return (f'Hotel(name={self.name},'
                f' {self.City.name if self.City else "No City Assigned"})')

    def __str__(self):
        return f"{self.name}, {self.City.name if self.City else 'No City Assigned'}"


class Airport(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    City = ForeignKey(City, on_delete=CASCADE, related_name="airports")

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Airports'

    def __repr__(self):
        return f'Airport(name={self.name}, city={self.City.name})'

    def __str__(self):
        return f"{self.name}, {self.City.name}"


class TravelInfo(Model):
    #'Departure and destination (city, airport, hotel'

    tour_name = CharField(max_length=200, null=False,
                          blank=False,
                          unique=True,
                          default='Tour name ')
    city = ForeignKey(City, on_delete=CASCADE,
                      related_name="city_travel_info")
    Hotel = ForeignKey(Hotel, on_delete=CASCADE,
                       related_name="hotels")

    departure_city = ForeignKey(City, on_delete=CASCADE,
                                related_name="departures",
                                null=True,
                                blank=True,
                                verbose_name="Departure (city)")

    departure_airport = ForeignKey(Airport, on_delete=CASCADE,
                                   related_name="departures_airport",
                                   null=True, blank=True,
                                   verbose_name="Departure (airport)")

    destination_city = ForeignKey(City, on_delete=CASCADE,
                                  related_name="arrivals",
                                  null=True,
                                  blank=True,
                                  verbose_name="Destination (city)")

    destination_airport = ForeignKey(Airport, on_delete=CASCADE,
                                     related_name="arrivals_airport",
                                     null=True,
                                     blank=True,
                                     verbose_name="Destination (airport)")

    description = models.TextField(null=True, blank=True)

    # Time details
    departure_date = DateField(verbose_name="Departure date",

                               null=True,
                               blank=True)
    return_date = DateField(verbose_name="Return date",
                            null=True,
                            blank=True)

    stay_duration = IntegerField(verbose_name="Duration of stay (days)",
                                 null=True,
                                 blank=True)

    created_at = models.DateTimeField(default=timezone.now,
                                      verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, null=True,
                                      verbose_name="Updated At")

    image = models.ImageField(upload_to="trip_images/", null=True, blank=True, verbose_name="Trip Image")

    # Meal type
    MEAL_TYPE_CHOICES = [
        ('BB', 'Bed & Breakfast'),
        ('HB', 'Half Board'),
        ('FB', 'Full Board'),
        ('AI', 'All Inclusive'),
    ]
    meal_type = CharField(
        max_length=2,
        choices=MEAL_TYPE_CHOICES,
        verbose_name="Meal type",
    )

    # Promotion
    is_promoted = models.BooleanField(default=False, verbose_name="Is promoted")

    # Number of seats
    adult_seats = IntegerField(verbose_name="Number of seats")
    child_seats = IntegerField(verbose_name="Number of seats for Kids")

    # Pricing
    price_per_adult = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price per passenger (czk)"
    )
    price_per_child = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price per Kid (czk)"
    )

    class Meta:
        verbose_name = "Travel Information"
        verbose_name_plural = "Travel Information"
        ordering = ["tour_name"]

    def __str__(self):
        departure_city = self.departure_city.name if self.departure_city else "Unknown Departure City"
        destination_city = self.destination_city.name if self.destination_city else "Unknown Destination City"
        return f"Trip: {self.tour_name} | Departure: {departure_city} -> {destination_city}"

    def clean(self):
        if self.departure_date and self.return_date and self.departure_date > self.return_date:
            raise ValidationError("Departure date cannot be later than return date.")

    def save(self, *args, **kwargs):
        # Automatically set the city based on hotel selection
        if self.Hotel:
            self.city = self.Hotel.City  # Assuming Hotel model has a 'city' field

            # Set the destination city to be the same as the hotel city, if not already set
            if not self.destination_city:
                self.destination_city = self.city

            # Automatically set the departure city to the same as the destination city, if not provided
            if not self.departure_city:
                self.departure_city = self.city

        # Automatically generate the tour_name if not set
        if not self.tour_name:
            self.tour_name = f"Tour to {self.city.name} - {self.Hotel.name}"

        super().save(*args, **kwargs)

    def formatted_departure_date(self):
        if self.departure_date:
            return self.departure_date.strftime('%d.%m.%Y')  # Den.Měsíc.Rok
        return '-'

    def formatted_return_date(self):
        if self.return_date:
            return self.return_date.strftime('%d.%m.%Y')  # Den.Měsíc.Rok
        return '-'

    def formatted_created_at(self):
        if self.created_at:
            return self.created_at.strftime('%d.%m.%Y')  # Den.Měsíc.Rok
        return '-'

    def formatted_updated_at(self):
        if self.updated_at:
            return self.updated_at.strftime('%d.%m.%Y')  # Den.Měsíc.Rok
        return '-'

    formatted_departure_date.short_description = 'Departure Date'  # Popis ve formátu adminu
    formatted_return_date.short_description = 'Return Date'
    formatted_created_at.short_description = 'Created At'
    formatted_updated_at.short_description = 'Updated At'

    @property
    def remaining_seats(self):
        return self.adult_seats + self.child_seats

    @property
    def is_last_minute(self):
        if self.departure_date:
            return (self.departure_date - timezone.now().date()).days <= 5
        return False

    @property
    def is_departing_soon(self):
        if self.departure_date:
            return (self.departure_date - timezone.now().date()).days > 5
        return False

    @staticmethod
    def get_top_selling_trips():
        return TravelInfo.objects.annotate(total_sales=models.Sum('purchases__adult_count') + models.Sum('purchases__child_count'))\
                                 .order_by('-total_sales')[:10]

    @staticmethod
    def get_trips_with_low_seats():
        trips = TravelInfo.objects.all()
        return [trip for trip in trips if trip.remaining_seats < 40]

    @staticmethod
    def get_last_minute_trips():
        return TravelInfo.objects.filter(departure_date__lte=timezone.now().date() + timezone.timedelta(days=5))

    @staticmethod
    def get_upcoming_trips():
        return TravelInfo.objects.filter(departure_date__gt=timezone.now().date() + timezone.timedelta(days=5))


class TourPurchase(models.Model):
    travel_info = models.ForeignKey(
        TravelInfo,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Trip"
    )
    adult_count = models.IntegerField(verbose_name="Passengers", default=0)
    child_count = models.IntegerField(verbose_name="Kids", default=0)
    total_quantity = models.IntegerField(verbose_name="Total Travelers", editable=False, default=0)
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Total Cost (CZK)",
        editable=False,
        default=0.00
    )
    customer_name = models.CharField(max_length=255, verbose_name="Customer Name", blank=False, null=False)
    customer_email = models.EmailField(verbose_name="Customer Email", blank=False, null=False)
    customer_phone = models.CharField(max_length=20, verbose_name="Customer Phone", blank=False, null=False)
    customer_address = models.TextField(verbose_name="Customer Address", blank=True, null=True)
    special_requests = models.TextField(verbose_name="Special Requests", blank=True, null=True)

    # New fields
    PAYMENT_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        verbose_name="Payment Method",
        default='card'
    )

    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        verbose_name="Order Status",
        default='pending'
    )
    travel_preferences = models.TextField(verbose_name="Travel Preferences", blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def save(self, *args, **kwargs):
        self.total_quantity = self.adult_count + self.child_count
        if self.travel_info:
            adult_price = self.travel_info.price_per_adult or 0
            child_price = self.travel_info.price_per_child or 0
            self.total_price = (self.adult_count * adult_price) + (self.child_count * child_price)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tour Purchase"
        verbose_name_plural = "Tour Purchases"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Purchase for {self.customer_name} | Total Price: {self.total_price} CZK | Status: {self.get_order_status_display()}"


class Payment(models.Model):
    tour_purchase = models.OneToOneField(
        TourPurchase,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name="Tour Purchase"
    )
    payment_date = models.DateTimeField(verbose_name="Payment Date", default=timezone.now)
    payment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Payment Amount",
        editable=False
    )
    payment_method = models.CharField(
        max_length=20,
        choices=TourPurchase.PAYMENT_CHOICES,
        verbose_name="Payment Method"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ],
        verbose_name="Payment Status",
        default='pending'
    )

    def save(self, *args, **kwargs):
        if not self.payment_amount:
            self.payment_amount = self.tour_purchase.total_price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Payment for {self.tour_purchase.customer_name} | Status: {self.get_payment_status_display()}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)  # Přidáme telefonní číslo
    message = models.TextField()
    address = models.TextField(blank=True, null=True)  # Volitelná adresa
    preferred_contact = models.CharField(
        max_length=20,
        choices=[('email', 'Email'), ('phone', 'Phone')],
        default='email',
        verbose_name="Preferred Contact Method"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} at {self.created_at}"
