from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.db.models import Sum, Avg, F, Count, Min, Max

from viewer.models import TravelInfo, Continent, TourPurchase, ContactMessage, Hotel, City
from django.template.defaulttags import register
from django import forms
import logging

logger = logging.getLogger(__name__)
from django.utils.timezone import now
from datetime import timedelta


def homepage(request):
    # Current date
    today = now().date()

    # Get promoted trips for the carousel
    promoted_trips = TravelInfo.objects.filter(is_promoted=True).order_by('-created_at')[:5]

    # Get last minute trips (departure within 5 days)
    last_minute_trips = TravelInfo.get_last_minute_trips()

    # Get trips with fewer than 40 seats remaining
    trips_with_low_seats = TravelInfo.get_trips_with_low_seats()

    # Get top-selling trips
    top_selling_trips = TravelInfo.get_top_selling_trips()

    # Get trips departing in more than 5 days
    upcoming_trips = TravelInfo.get_upcoming_trips()

    # Render the template with context
    return render(request, 'homepage.html', {
        'promoted_trips': promoted_trips,
        'last_minute_trips': last_minute_trips,
        'trips_with_low_seats': trips_with_low_seats,
        'top_selling_trips': top_selling_trips,
        'upcoming_trips': upcoming_trips,
    })


def all_trips(request):
    trips = TravelInfo.objects.all()
    return render(request, "Trips.html", {"trips": trips})


def trip_list(request):
    trips = TravelInfo.objects.all()
    return render(request, 'trip_list.html', {'trips': trips})


def trip_detail(request, trip_id):
    trip = get_object_or_404(TravelInfo, pk=trip_id)

    # Výpočet zbývajících míst (příklad: pokud existují rezervace)
    reserved_adults = trip.purchases.aggregate(Sum('adult_count'))['adult_count__sum'] or 0
    reserved_kids = trip.purchases.aggregate(Sum('child_count'))['child_count__sum'] or 0

    remaining_adult_seats = max(trip.adult_seats - reserved_adults, 0)
    remaining_child_seats = max(trip.child_seats - reserved_kids, 0)

    context = {
        'trip': trip,
        'remaining_adult_seats': remaining_adult_seats,
        'remaining_child_seats': remaining_child_seats,
    }

    return render(request, 'trip_detail.html', context)


def purchase_trip(request, trip_id):
    trip = get_object_or_404(TravelInfo, pk=trip_id)
    total_price = 0

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        try:
            adults = int(request.POST.get('adults', 0))
            kids = int(request.POST.get('kids', 0))
        except ValueError:
            adults, kids = 0, 0

        errors = []
        if not name:
            errors.append("Jméno je povinné.")
        if not email:
            errors.append("E-mail je povinný.")
        if adults <= 0 and kids <= 0:
            errors.append("Musíte zadat alespoň jednoho účastníka.")

        # Spočítat celkovou cenu na backendu
        total_price = (trip.price_per_adult * adults) + (trip.price_per_child * kids)

        if errors:
            return render(request, 'purchase_form.html', {
                'trip': trip,
                'errors': errors,
                'form_data': {
                    'name': name,
                    'email': email,
                    'adults': adults,
                    'kids': kids,
                },
                'total_price': total_price,
            })

        # Uložení rezervace
        purchase = TourPurchase(
            travel_info=trip,
            adult_count=adults,
            child_count=kids,
            customer_name=name,
            customer_email=email
        )
        purchase.save()

        return render(request, 'purchase_success.html', {
            'purchase': purchase,
            'trip': trip,
            'total_price': total_price,
        })

    return render(request, 'purchase_form.html', {
        'trip': trip,
        'form_data': {
            'name': '',
            'email': '',
            'adults': 0,
            'kids': 0,
        },
        'errors': [],
        'total_price': total_price,
    })


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message', 'preferred_contact']

    # Optional: Add custom styling or validation rules
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def thank_you(request):
    return render(request, 'thank_you.html')


def hotels(request):
    # Načtení všech hotelů a aplikace filtrů
    hotels_list = Hotel.objects.all().order_by('name')  # Načti hotely
    city_filter = request.GET.get('city')  # Získání filtru pro město
    stars_filter = request.GET.get('stars')  # Získání filtru pro hvězdičky
    search_query = request.GET.get('search')  # Získání filtru pro hledání

    # Filtr podle města
    if city_filter:
        hotels_list = hotels_list.filter(City__name__iexact=city_filter)

    # Filtr podle hvězdiček
    if stars_filter:
        try:
            stars_filter = int(stars_filter)
            hotels_list = hotels_list.filter(Stars=stars_filter)
        except ValueError:
            pass  # Pokud je hodnota filtru hvězdiček neplatná, ignorujeme ji

    # Filtr podle názvu hotelu
    if search_query:
        hotels_list = hotels_list.filter(name__icontains=search_query)

    # Načtení všech měst pro výběr v šabloně
    cities = City.objects.all()

    # Stránkování
    paginator = Paginator(hotels_list, 6)  # 6 hotelů na stránku
    page = request.GET.get('page')
    try:
        hotels = paginator.page(page)
    except PageNotAnInteger:
        hotels = paginator.page(1)
    except EmptyPage:
        hotels = paginator.page(paginator.num_pages)

    context = {
        'hotels': hotels,
        'cities': cities,
        'city_filter': city_filter,
        'stars_filter': stars_filter,
        'search_query': search_query,
    }
    return render(request, 'hotels.html', context)


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    cities = City.objects.all()
    travel_infos = TravelInfo.objects.filter(Hotel=hotel)
    context = {
        'hotel': hotel,
        'cities': cities,
        'travel_infos': travel_infos
    }
    return render(request, 'hotel_detail.html', context)


@register.filter
def generate_range(value):
    """
    Vytvoří range objekt pro iteraci v šabloně.
    Pokud je hodnota neplatná nebo není číslo, vrací prázdný range.
    """
    try:
        value = int(value)
        return range(max(value, 0))  # Ujisti se, že hodnota není záporná
    except (ValueError, TypeError):
        return range(0)