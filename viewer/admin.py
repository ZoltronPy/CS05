from django.contrib import admin
from django.contrib.admin import AdminSite
from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase


# Inline pro státy
class CountryInline(admin.TabularInline):
    model = Country
    extra = 1  # Počet prázdných formulářů pro přidání nového státu


# Inline pro města
class CityInline(admin.TabularInline):
    model = City
    extra = 1  # Počet prázdných formulářů pro přidání nového města


class HotelInline(admin.TabularInline):
    model = Hotel  # Definujeme, že inline se týká modelu Hotel
    extra = 1  # Počet prázdných formulářů pro přidání hotelu


# Custom Admin pro Continent
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [CountryInline]  # Přidá inline pro státy při editaci kontinentu


# Custom Admin pro Country
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent')
    inlines = [CityInline]  # Přidá inline pro města při editaci státu


# Admin pro City
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country',)
    inlines = [HotelInline]


# Admin pro Hotel
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'City')
    search_fields = ('name', 'City__name')


# Admin pro Airport
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'City')


# Admin pro TravelInfo
class TravelInfoAdmin(admin.ModelAdmin):
    list_display = (
        "tour_name", "departure_city", "destination_city",
        "formatted_departure_date", "formatted_return_date",
        "price_per_adult", "price_per_child", "formatted_created_at", "formatted_updated_at",
    )
    search_fields = ("tour_name", "departure_city__name", "destination_city__name")
    list_filter = ("departure_date", "return_date", "meal_type", "is_promoted")


from django.contrib import admin
from django.contrib.admin import AdminSite
from viewer.models import Continent, Country, City, Hotel, Airport, TravelInfo, TourPurchase

# Inline pro státy
class CountryInline(admin.TabularInline):
    model = Country
    extra = 1  # Počet prázdných formulářů pro přidání nového státu

# Inline pro města
class CityInline(admin.TabularInline):
    model = City
    extra = 1  # Počet prázdných formulářů pro přidání nového města

class HotelInline(admin.TabularInline):
    model = Hotel  # Definujeme, že inline se týká modelu Hotel
    extra = 1  # Počet prázdných formulářů pro přidání hotelu

# Custom Admin pro Continent
class ContinentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [CountryInline]  # Přidá inline pro státy při editaci kontinentu

# Custom Admin pro Country
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'continent')
    inlines = [CityInline]  # Přidá inline pro města při editaci státu

# Admin pro City
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country',)
    inlines = [HotelInline]

# Admin pro Hotel
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'City')

    # Ensure City is always displayed properly
    def City(self, obj):
        return obj.City.name if obj.City else 'No City Assigned'

    search_fields = ('name', 'City__name')

# Admin pro Airport
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'City')

# Admin pro TravelInfo
class TravelInfoAdmin(admin.ModelAdmin):
    list_display = (
        "tour_name", "departure_city", "destination_city",
        "formatted_departure_date", "formatted_return_date",
        "price_per_adult", "price_per_child", "formatted_created_at", "formatted_updated_at",
    )
    search_fields = ("tour_name", "departure_city__name", "destination_city__name")
    list_filter = ("departure_date", "return_date", "meal_type", "is_promoted")

# Admin pro TourPurchase
class TourPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'get_tour_name', 'adult_count', 'child_count', 'total_quantity', 'total_price', 'formatted_created_at',
        'formatted_updated_at'
    )
    search_fields = ('travel_info__tour_name',)
    list_filter = ('travel_info__tour_name',)

    def get_tour_name(self, obj):
        return obj.travel_info.tour_name if obj.travel_info else 'No Tour Name Available'

    get_tour_name.short_description = 'Tour Name'

# Vlastní Admin Site
class CustomAdminSite(AdminSite):
    site_header = "Admin - Custom"
    site_title = "Admin Panel"
    index_title = "Welcome to the Admin Panel"

# Vytvoření instance pro nový Admin Site
custom_admin_site = CustomAdminSite(name='Admin SITE')

# Registrace adminů pro modely
custom_admin_site.register(Continent, ContinentAdmin)
custom_admin_site.register(Country, CountryAdmin)
custom_admin_site.register(City, CityAdmin)
custom_admin_site.register(Hotel, HotelAdmin)
custom_admin_site.register(Airport, AirportAdmin)
custom_admin_site.register(TravelInfo, TravelInfoAdmin)
custom_admin_site.register(TourPurchase, TourPurchaseAdmin)
