from django.contrib import admin

from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase, Traveler

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Airport)
admin.site.register(TravelInfo)
admin.site.register(TourPurchase)
admin.site.register(Traveler)
