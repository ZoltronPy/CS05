from django.shortcuts import render
from django.shortcuts import get_object_or_404
from viewer.models import TravelInfo, Continent
from viewer.models import TourPurchase


def homepage(request):
    promoted_trips = TravelInfo.objects.filter(is_promoted=True).order_by('-created_at')[:5]
    continents = Continent.objects.prefetch_related('countries__cities')
    return render(request, 'homepage.html', {'promoted_trips': promoted_trips, 'continents': continents})


def all_trips(request):
    trips = TravelInfo.objects.all()
    context = {
        "trips": trips,
    }
    return render(request, "Trips.html", context)


def trip_list(request):
    trips = TravelInfo.objects.all()
    return render(request, 'trip_list.html', {'trips': trips})


def trip_detail(request, trip_id):
    trip = get_object_or_404(TravelInfo, id=trip_id)
    return render(request, 'trip_detail.html', {'trip': trip})


from django.shortcuts import render, get_object_or_404, redirect
from viewer.models import TravelInfo, TourPurchase

def purchase_trip(request, trip_id=None):
    # Pokud je metoda GET, zobrazí formulář
    if request.method == 'GET':
        # Získání detailu výletu
        trip = get_object_or_404(TravelInfo, pk=trip_id)
        return render(request, 'purchase_form.html', {'trip': trip})

    # Pokud je metoda POST, uloží objednávku
    elif request.method == 'POST':
        # Získání dat z formuláře
        trip_id = request.POST.get('trip_id')
        name = request.POST.get('name')  # Jméno zákazníka
        email = request.POST.get('email')  # Email zákazníka
        adults = int(request.POST.get('adults', 0))
        kids = int(request.POST.get('kids', 0))

        trip = get_object_or_404(TravelInfo, pk=trip_id)

        # Vytvoření objednávky
        purchase = TourPurchase(
            travel_info=trip,
            adult_count=adults,
            child_count=kids,
            customer_name=name,  # Přidání jména zákazníka
            customer_email=email,  # Přidání emailu zákazníka
        )
        purchase.save()

        # Přesměrování nebo zobrazení potvrzení objednávky
        return render(request, 'purchase_success.html', {'purchase': purchase})


