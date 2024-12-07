from django.shortcuts import render
from django.shortcuts import get_object_or_404
from viewer.models import TravelInfo
from viewer.models import TourPurchase


def homepage(request):
    promoted_trips = TravelInfo.objects.filter(is_promoted=True).order_by('-created_at')[:5]
    return render(request, 'homepage.html', {'promoted_trips': promoted_trips})
def all_trips(request):
    trips = TravelInfo.objects.all()  # Předpokládáme, že načítáš všechny zájezdy
    context = {
        "trips": trips,
    }
    return render(request, "Trips.html", context)

def trip_list(request):
    trips = TravelInfo.objects.all()
    return render(request, 'trip_list.html', {'trips': trips})


def trip_detail(request, trip_id):
    trip = get_object_or_404(TravelInfo, pk=trip_id)
    return render(request, 'trip_detail.html', {'trip': trip})


def purchase_trip(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        adults = int(request.POST.get('adults', 0))
        kids = int(request.POST.get('kids', 0))

        trip = get_object_or_404(TravelInfo, pk=trip_id)
        purchase = TourPurchase(
            travel_info=trip,
            adult_count=adults,
            child_count=kids,
        )
        purchase.save()

        return render(request, 'purchase_success.html', {'purchase': purchase})
    else:
        trips = TravelInfo.objects.all()
        return render(request, 'purchase_form.html', {'trips': trips})

