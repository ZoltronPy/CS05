from django.shortcuts import render
from viewer.models import TravelInfo


def home(request):
    return render(request, 'home.html')


def all_trips(request):
    trips = TravelInfo.objects.all()  # Předpokládáme, že načítáš všechny zájezdy
    context = {
        "trips": trips,
    }
    return render(request, "Trips.html", context)

