from django.contrib import admin

from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Hotel)
admin.site.register(Airport)
admin.site.register(TravelInfo)
@admin.register(TourPurchase)
class TourPurchaseAdmin(admin.ModelAdmin):
    list_display = ("travel_info", "adult_count", "child_count", "total_quantity", "total_price", "created_at")
    search_fields = ("travel_info__tour_name",)
    list_filter = ("created_at",)
