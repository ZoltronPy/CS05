from django.shortcuts import render
from viewer.models import TravelInfo


def all_trips(request):
    trips = TravelInfo.objects.all()  # Předpokládáme, že načítáš všechny zájezdy
    context = {
        "trips": trips,
    }
    return render(request, "Trips.html", context)

