from django.contrib import admin
from django.contrib.admin import AdminSite
from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase, ContactMessage, Payment

# Custom Admin Site
from django.contrib import admin
from django.contrib.admin import AdminSite
from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase, ContactMessage, Payment


# Vlastní Admin Site
class CustomAdminSite(AdminSite):
    site_header = "Admin - Custom"
    site_title = "Admin Panel"
    index_title = "Welcome to the Admin Panel"


# Vytvoření instance pro nový Admin Site
custom_admin_site = CustomAdminSite(name='Admin SITE')


# Inline pro státy
class CountryInline(admin.TabularInline):
    model = Country
    extra = 1


# Inline pro města
class CityInline(admin.TabularInline):
    model = City
    extra = 1


# Inline pro hotely
class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 1


# Custom Admin pro Continent
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [CountryInline]


# Custom Admin pro Country
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent')
    inlines = [CityInline]


# Admin pro City
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    inlines = [HotelInline]


# Admin pro Hotel
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_city')

    def get_city(self, obj):
        return obj.city.name if obj.city else 'No City Assigned'

    get_city.short_description = 'City'

    search_fields = ('name', 'city__name')


# Admin pro Airport
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_city')

    def get_city(self, obj):
        return obj.city.name if obj.city else 'No City Assigned'

    get_city.short_description = 'City'

    search_fields = ('name', 'city__name')


# Admin pro TravelInfo
class TravelInfoAdmin(admin.ModelAdmin):
    list_display = (
        "tour_name", "departure_city", "destination_city",
        "formatted_departure_date", "formatted_return_date",
        "price_per_adult", "price_per_child", "formatted_created_at", "formatted_updated_at"
    )
    search_fields = ("tour_name", "departure_city__name", "destination_city__name")
    list_filter = ("departure_date", "return_date", "meal_type", "is_promoted")


# Admin pro TourPurchase
class TourPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'get_tour_name', 'get_customer_name', 'adult_count', 'child_count',
        'total_quantity', 'total_price', 'customer_email', 'customer_phone', 'customer_address', 'special_requests',
        'formatted_created_at'
    )
    search_fields = ('travel_info__tour_name', 'customer_name', 'customer_email', 'customer_phone')
    list_filter = ('travel_info__destination_city__name', 'travel_info__departure_date', 'created_at')

    def get_tour_name(self, obj):
        return obj.travel_info.tour_name if obj.travel_info else "No Tour Name Available"

    get_tour_name.short_description = 'Tour Name'

    def get_customer_name(self, obj):
        return obj.customer_name or "Not Provided"

    get_customer_name.short_description = 'Customer Name'

    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M:%S') if obj.created_at else "-"

    formatted_created_at.short_description = 'Created At'

    readonly_fields = ('total_quantity', 'total_price', 'created_at', 'updated_at')


# Admin pro ContactMessage
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'message')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


# Admin pro Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tour_purchase', 'payment_amount', 'payment_status', 'payment_method')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('tour_purchase__customer_name',)


# Registrace adminů pro modely
custom_admin_site.register(Continent, ContinentAdmin)
custom_admin_site.register(Country, CountryAdmin)
custom_admin_site.register(City, CityAdmin)
custom_admin_site.register(Hotel, HotelAdmin)
custom_admin_site.register(Airport, AirportAdmin)
custom_admin_site.register(TravelInfo, TravelInfoAdmin)
custom_admin_site.register(TourPurchase, TourPurchaseAdmin)
custom_admin_site.register(ContactMessage, ContactMessageAdmin)
