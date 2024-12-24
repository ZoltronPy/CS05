from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.db.models import Sum, Q
from django import forms
from django.utils.timezone import now
from datetime import timedelta
import logging

from viewer.models import TravelInfo, Country, TourPurchase, ContactMessage, Hotel, City

logger = logging.getLogger(__name__)


def homepage(request):
    promoted_trips = TravelInfo.objects.filter(is_promoted=True).order_by('-created_at')[:5]
    last_minute_trips = TravelInfo.get_last_minute_trips()
    trips_with_low_seats = TravelInfo.get_trips_with_low_seats()
    top_selling_trips = TravelInfo.get_top_selling_trips()
    upcoming_trips = TravelInfo.get_upcoming_trips()

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

    # Dynamický obsah boxů
    sales_text = "Check out our current promotions and save big!"
    last_minute_text = "Hurry up! Last-minute deals are waiting for you!"

    return render(request, 'trip_list.html', {
        'trips': trips,
        'sales_text': sales_text,
        'last_minute_text': last_minute_text,
    })


def trip_detail(request, trip_id):
    trip = get_object_or_404(TravelInfo, pk=trip_id)

    reserved_adults = trip.purchases.aggregate(Sum('adult_count'))['adult_count__sum'] or 0
    reserved_kids = trip.purchases.aggregate(Sum('child_count'))['child_count__sum'] or 0

    remaining_adult_seats = max(trip.adult_seats - reserved_adults, 0)
    remaining_child_seats = max(trip.child_seats - reserved_kids, 0)

    return render(request, 'Tour_details.html', {
        'trip': trip,
        'remaining_adult_seats': remaining_adult_seats,
        'remaining_child_seats': remaining_child_seats,
    })


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
            errors.append("Name is required.")
        if not email:
            errors.append("Email is required.")
        if adults <= 0 and kids <= 0:
            errors.append("At least one traveler must be specified.")

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
    hotels_list = Hotel.objects.all().order_by('name')
    city_filter = request.GET.get('city')
    stars_filter = request.GET.get('stars')
    search_query = request.GET.get('search')

    if city_filter:
        hotels_list = hotels_list.filter(City__name__iexact=city_filter)

    if stars_filter:
        try:
            stars_filter = int(stars_filter)
            hotels_list = hotels_list.filter(Stars=stars_filter)
        except ValueError:
            pass

    if search_query:
        hotels_list = hotels_list.filter(name__icontains=search_query)

    cities = City.objects.all()

    paginator = Paginator(hotels_list, 6)
    page = request.GET.get('page')
    try:
        hotels = paginator.page(page)
    except PageNotAnInteger:
        hotels = paginator.page(1)
    except EmptyPage:
        hotels = paginator.page(paginator.num_pages)

    return render(request, 'hotels.html', {
        'hotels': hotels,
        'cities': cities,
        'city_filter': city_filter,
        'stars_filter': stars_filter,
        'search_query': search_query,
    })


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    travel_infos = TravelInfo.objects.filter(Hotel=hotel)

    return render(request, 'hotel_detail.html', {
        'hotel': hotel,
        'travel_infos': travel_infos,
    })


def all_offers(request):
    country_filter = request.GET.get('country')
    price_filter = request.GET.get('price_range')
    search_query = request.GET.get('search')

    offers = TravelInfo.objects.all()

    if country_filter:
        offers = offers.filter(destination_city__country_id=country_filter)

    if price_filter:
        try:
            min_price, max_price = map(int, price_filter.split('-'))
            offers = offers.filter(price_per_adult__gte=min_price, price_per_adult__lte=max_price)
        except (ValueError, TypeError):
            pass

    if search_query:
        offers = offers.filter(
            Q(tour_name__icontains=search_query) |
            Q(destination_city__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    countries = Country.objects.all()

    return render(request, 'all_offers.html', {
        'offers': offers,
        'countries': countries,
        'country_filter': country_filter,
        'price_filter': price_filter,
        'search_query': search_query,
    })


def offer_detail(request, pk):
    offer = get_object_or_404(TravelInfo, pk=pk)
    return render(request, 'Tour_details.html', {'offer': offer})


def search_results(request):
    query = request.GET.get('q')
    results = TravelInfo.objects.none()

    if query:
        results = TravelInfo.objects.filter(
            Q(tour_name__icontains=query) |
            Q(destination_city__name__icontains=query) |
            Q(Hotel__name__icontains=query)
        )

    return render(request, 'search_results.html', {'results': results, 'query': query})
