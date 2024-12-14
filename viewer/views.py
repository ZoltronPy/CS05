from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.db.models import Sum, Avg, F, Count, Min, Max

from viewer.models import TravelInfo, Continent, TourPurchase, ContactMessage, Hotel
from django import forms
import logging
logger = logging.getLogger(__name__)


def homepage(request):
    promoted_trips = TravelInfo.objects.filter(is_promoted=True).order_by('-created_at')[:5]
    continents = Continent.objects.prefetch_related('countries__cities')
    return render(request, 'homepage.html', {
        'promoted_trips': promoted_trips,
        'continents': continents
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


class HotelsViewTemplateView(TemplateView):
    template_name = "hotels.html"
    extra_context = {'hotels': Hotel.objects.all(), }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotels'] = Hotel.objects.all()
        return context
