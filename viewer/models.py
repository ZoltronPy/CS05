from django.db import models
from django.db.models import Model, CharField, ForeignKey, CASCADE, TextField, IntegerField


#vytvoření kontinetu
class Continent(Model):
    name = CharField(max_length=32, unique=True, null=False, blank=False)

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
    City = ForeignKey(City, on_delete=CASCADE, related_name="hotels")

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


