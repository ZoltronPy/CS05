from django.core.exceptions import ValidationError
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

    tour_name = CharField(max_length=32, null=False,
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





class TourPurchase(Model):
    travel_info = ForeignKey(
        TravelInfo,
        on_delete=CASCADE,
        related_name="purchases",
        verbose_name="Trip"
    )
    adult_count = IntegerField(verbose_name="Passengers", default=0)
    child_count = IntegerField(verbose_name="Kids", default=0)
    total_quantity = IntegerField(verbose_name="Total Travelers", editable=False, default=0)
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Total Cost (czk)",
        editable=False,
        default=0.00
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    # Metoda pro získání názvu zájezdu
    def get_tour_name(self):
        return self.travel_info.tour_name if self.travel_info else "No Tour Name"

    get_tour_name.short_description = "Tour Name"

    # Formátované datumy pro administraci
    def formatted_created_at(self):
        return self.created_at.strftime('%d.%m.%Y') if self.created_at else '-'

    formatted_created_at.short_description = 'Created At'

    def formatted_updated_at(self):
        return self.updated_at.strftime('%d.%m.%Y') if self.updated_at else '-'

    formatted_updated_at.short_description = 'Updated At'

    # Reprezentace objektu
    def __str__(self):
        if self.travel_info:
            return f"Trip: {self.travel_info.tour_name} | Adults: {self.adult_count}, Kids: {self.child_count}"
        return "No tour information"

    # Uložení objektu se spočítáním celkových hodnot
    def save(self, *args, **kwargs):
        # Výpočet celkového množství cestujících
        self.total_quantity = self.adult_count + self.child_count

        # Výpočet celkové ceny
        if self.travel_info:
            adult_price = self.travel_info.price_per_adult or 0
            child_price = self.travel_info.price_per_child or 0
            self.total_price = (self.adult_count * adult_price) + (self.child_count * child_price)

        logger.debug(f"Saving TourPurchase: {self.total_quantity} travelers, total price {self.total_price}")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tour Purchase"
        verbose_name_plural = "Tour Purchases"
        ordering = ["-created_at"]


class ContinentCountryCity(models.Model):
    continent_name = models.CharField(max_length=32, unique=True)
    country_name = models.CharField(max_length=50)
    international_code = models.CharField(max_length=10, blank=True, null=True)
    city_name = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.city_name}, {self.country_name}, {self.continent_name}"
