from .models import TravelInfo


def offers_processor(request):
    last_minute_offers = TravelInfo.get_last_minute_trips()
    first_minute_offers = TravelInfo.get_upcoming_trips()
    return {
        'last_minute_offers': last_minute_offers,
        'first_minute_offers': first_minute_offers,
    }
