from django.utils import timezone
from datetime import timedelta

from django.contrib import admin
from django.contrib.admin import AdminSite
from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase


class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent')


class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'Country')


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'City')


class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'City')


admin.site.register(Continent, ContinentAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Airport, AirportAdmin)


class TravelInfoAdmin(admin.ModelAdmin):
    list_display = (
        "tour_name", "departure_city", "destination_city",
        "formatted_departure_date", "formatted_return_date",
        "price_per_adult", "price_per_child", "formatted_created_at", "formatted_updated_at",
    )
    search_fields = ("tour_name", "departure_city__name", "destination_city__name")
    list_filter = ("departure_date", "return_date", "meal_type", "is_promoted")


admin.site.register(TravelInfo, TravelInfoAdmin)


class TourPurchaseAdmin(admin.ModelAdmin):
    list_display = ("travel_info", "adult_count", "child_count", "total_quantity",
                    "total_price", "formatted_created_at", "formatted_updated_at")
    search_fields = ("travel_info__tour_name",)
    list_filter = ("created_at",)


admin.site.register(TourPurchase, TourPurchaseAdmin)


class CustomAdminSite(AdminSite):
    site_header = "My Custom Admin"
    site_title = "Admin Panel"
    index_title = "Welcome to the Admin Panel"


# Vytvoření instance pro nový Admin Site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Registrace všech admin modelů
custom_admin_site.register(Continent, ContinentAdmin)
custom_admin_site.register(Country, CountryAdmin)
custom_admin_site.register(City, CityAdmin)
custom_admin_site.register(Hotel, HotelAdmin)
custom_admin_site.register(Airport, AirportAdmin)

custom_admin_site.register(TravelInfo, TravelInfoAdmin)
custom_admin_site.register(TourPurchase, TourPurchaseAdmin)


