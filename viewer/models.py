from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import now

from django.db import models
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, IntegerField, DateField


#'vytvoření kontinetu'
class Continent(Model):
    name = CharField(max_length=32, unique=True, null=False, blank=False, db_index=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'Continent(name={self.name})'

    def __str__(self):
        return f"{self.name}"


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
        return f'Country(name={self.name})'

    def __str__(self):
        return self.name


# Město
class City(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    Country = ForeignKey(Country, on_delete=CASCADE, null=False, blank=False,
                         related_name="cities")
    description = TextField(null=True, blank=True)

    hotels = models.ManyToManyField('viewer.Hotel', related_name='cities_set', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cities'

    def __repr__(self):
        return f'City(name={self.name})'

    def __str__(self):
        return self.name


class Hotel(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    Stars = IntegerField(null=True, blank=True, default=0)
    Description = TextField(null=True, blank=True)

    City = ForeignKey(City, on_delete=CASCADE, related_name="city_hotels", blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Hotels'

    def __repr__(self):
        return f'Hotel(name={self.name})'

    def __str__(self):
        return self.name


class Airport(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    City = ForeignKey(City, on_delete=CASCADE, related_name="airports")

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Airports'

    def __repr__(self):
        return f'Airport(name={self.name})'

    def __str__(self):
        return self.name


class TravelInfo(Model):
    #'Departure and destination (city, airport, hotel'

    tour_name = CharField(max_length=32, null=False, blank=False, unique=True, default='Default Tour Name')

    departure_city = ForeignKey(City, on_delete=CASCADE, related_name="departures", null=True, blank=True,
                                verbose_name="Departure (city)")
    destination_hotels = models.ManyToManyField(Hotel, related_name='travel_infos', blank=True)

    departure_airport = ForeignKey(Airport, on_delete=CASCADE, related_name="departures_airport", null=True, blank=True,
                                   verbose_name="Departure (airport)")
    destination_city = ForeignKey(City, on_delete=CASCADE, related_name="arrivals", null=True, blank=True,
                                  verbose_name="Destination (city)")
    destination_airport = ForeignKey(Airport, on_delete=CASCADE, related_name="arrivals_airport", null=True, blank=True,
                                     verbose_name="Destination (airport)")
    description = models.TextField(null=True, blank=True)

    # Time details
    departure_date = DateField(verbose_name="Departure date", null=True, blank=True)
    return_date = DateField(verbose_name="Return date", null=True, blank=True)
    stay_duration = IntegerField(verbose_name="Duration of stay (days)", null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name="Updated At")

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

    # Pricing
    price_per_adult = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price per adult (CZK)"
    )
    price_per_child = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price per child (CZK)"
    )

    # Promotion
    is_promoted = models.BooleanField(default=False, verbose_name="Is promoted")

    # Number of seats
    adult_seats = IntegerField(verbose_name="Number of seats for adults")
    child_seats = IntegerField(verbose_name="Number of seats for children")

    class Meta:
        verbose_name = "Travel Information"
        verbose_name_plural = "Travel Information"
        ordering = ["tour_name"]

    def __str__(self):
        departure = self.departure_city or self.departure_airport or "Unknown departure"
        destination = (self.destination_city or self.destination_hotel or
                       self.destination_airport or "Unknown destination")
        return (f"{self.departure_city or self.departure_airport} -> "
                f"{self.destination_city or self.destination_hotel or self.destination_airport} "
                f"({self.departure_date} - {self.return_date})")

    def clean(self):
        if self.departure_date and self.return_date and self.departure_date > self.return_date:
            raise ValidationError("Departure date cannot be later than return date.")


class TourPurchase(Model):
    travel_info = ForeignKey(TravelInfo, on_delete=CASCADE, related_name="purchases",
                             verbose_name="Trip")
    adult_count = IntegerField(verbose_name="passengers", default=0)
    child_count = IntegerField(verbose_name="KIDS", default=0)
    total_quantity = IntegerField(verbose_name="Total Travelers", editable=False, default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Total Cost (czk)",
                                      editable=False, default=0.00)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="updated at ")

    def formatted_created_at(self):
        if self.created_at:
            return self.created_at.strftime('%d.%m.%Y')  # Den.Měsíc.Rok
        return '-'

    def formatted_updated_at(self):
        if self.updated_at:
            return self.updated_at.strftime('%d.%m.%Y')  # Den.Měsíc.Rok
        return '-'

    formatted_created_at.short_description = 'created at'
    formatted_updated_at.short_description = 'updated_at'

    class Meta:
        verbose_name = "Tour Purchase"
        verbose_name_plural = "Tour Purchases"
        ordering = ["-created_at"]

    def __str__(self):
        return (f"Purchase: {self.travel_info.tour_name} | "
                f"Adult: {self.adult_count}, Kids: {self.child_count}")


def save(self, *args, **kwargs):
    # Automatický výpočet celkového množství
    self.total_quantity = self.adult_count + self.child_count

    # Výpočet celkové ceny
    adult_price = self.travel_info.price_per_adult or 0
    child_price = self.travel_info.price_per_child or 0
    self.total_price = (self.adult_count * adult_price) + (self.child_count * child_price)

    super().save(*args, **kwargs)

