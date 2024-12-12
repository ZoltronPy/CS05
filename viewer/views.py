from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView

from viewer.models import TravelInfo, Continent, TourPurchase, ContactMessage, Hotel
from django import forms


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
    trip = get_object_or_404(TravelInfo, id=trip_id)
    return render(request, 'trip_detail.html', {'trip': trip})


def purchase_trip(request, trip_id):
    trip = get_object_or_404(TravelInfo, pk=trip_id)

    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        adults = int(request.POST.get('adults', 0))
        kids = int(request.POST.get('kids', 0))

        # Validation for required fields
        if not name or not email:
            return render(request, 'purchase_form.html', {
                'trip': trip,
                'error': 'Name and Email are required.',
            })

        # Create the purchase object
        purchase = TourPurchase(
            travel_info=trip,
            adult_count=adults,
            child_count=kids,
            customer_name=name,
            customer_email=email
        )
        purchase.save()

        return render(request, 'purchase_success.html', {'purchase': purchase})

    # If GET request, render the purchase form
    return render(request, 'purchase_form.html', {'trip': trip})


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
