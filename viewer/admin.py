from datetime import timedelta

from django.contrib import admin

from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Airport)


@admin.register(TravelInfo)
class TravelInfoAdmin(admin.ModelAdmin):
    list_display = (
        "tour_name", "departure_city", "destination_city", "departure_date", "return_date", "price_per_adult",
        "price_per_child")
    search_fields = ("tour_name", "departure_city__name", "destination_city__name")
    list_filter = ("departure_date", "return_date", "meal_type", "is_promoted")


@admin.register(TourPurchase)
class TourPurchaseAdmin(admin.ModelAdmin):
    list_display = ("travel_info", "adult_count", "child_count", "total_quantity", "total_price", "created_at")
    search_fields = ("travel_info__tour_name",)
    list_filter = ("created_at",)

