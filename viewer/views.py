from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib import messages
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.db.models import Sum, Q
from django import forms
from django.utils.timezone import now
from datetime import timedelta
import logging

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Employee
from .forms import EmployeeForm, OrderForm, TravelInfoForm

from viewer.models import TravelInfo, Country, TourPurchase, ContactMessage, Hotel, City

logger = logging.getLogger(__name__)


def homepage(request):
    promoted_trips = TravelInfo.objects.filter(is_promoted=True).order_by('-created_at')[:5]
    last_minute_trips = TravelInfo.get_last_minute_trips()
    trips_with_low_seats = TravelInfo.get_trips_with_low_seats()
    top_selling_trips = TravelInfo.get_top_selling_trips()
    upcoming_trips = TravelInfo.get_upcoming_trips()

    # Zjistit roli uživatele, pokud je přihlášen
    user_role = None
    is_manager_or_senior = False
    if request.user.is_authenticated and hasattr(request.user, "employee_profile"):
        user_role = request.user.employee_profile.role
        is_manager_or_senior = user_role in ["manager", "senior"]

    return render(request, 'homepage.html', {
        'promoted_trips': promoted_trips,
        'last_minute_trips': last_minute_trips,
        'trips_with_low_seats': trips_with_low_seats,
        'top_selling_trips': top_selling_trips,
        'upcoming_trips': upcoming_trips,
        'is_manager_or_senior': is_manager_or_senior,  # Přidání této hodnoty
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

    return render(request, 'Trip_detail.html', {
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
    return render(request, 'Trip_detail.html', {'offer': offer})


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


# Kontrola, jestli je uživatel Manager
def is_manager(user):
    return user.is_authenticated and hasattr(user, 'employee_profile') and user.employee_profile.role == 'manager'


@login_required
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})


@login_required
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    assigned_trips = employee.travel_infos.all()   # Přidělené zájezdy
    orders = TourPurchase.objects.filter(travel_info__in=assigned_trips)  # Objednávky spojené se zájezdy

    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'assigned_trips': assigned_trips,
        'orders': orders,
    })


@login_required
@user_passes_test(is_manager)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('employee_list')
            except Exception as e:
                form.add_error(None, f"Error saving employee: {e}")
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})


@login_required
@user_passes_test(is_manager)
def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form, 'action': 'Edit'})


@login_required
@user_passes_test(is_manager)
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


@login_required
def order_list(request, employee_id=None):
    if employee_id:
        employee = get_object_or_404(Employee, id=employee_id)
        assigned_trips = TravelInfo.objects.filter(assigned_to=employee)
        print(f"Assigned Trips: {assigned_trips}")  # Ladicí výstup
        orders = TourPurchase.objects.filter(travel_info__in=assigned_trips)
        print(f"Orders: {orders}")  # Ladicí výstup
    else:
        orders = TourPurchase.objects.all()

    return render(request, 'orders/order_list.html', {
        'orders': orders
    })


@login_required
def order_detail(request, order_id):
    # Detail objednávky s možností úpravy
    order = get_object_or_404(TourPurchase, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_detail.html', {'form': form, 'order': order})


@login_required
def order_create(request):
    # Přidání nové objednávky
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})


@login_required
def order_delete(request, order_id):
    # Smazání objednávky
    order = get_object_or_404(TourPurchase, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})


@login_required
@user_passes_test(
    lambda user: hasattr(user, 'employee_profile') and user.employee_profile.role in ['manager', 'senior'])
def contact_message_list(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'contact_messages/message_list.html', {'messages': messages})


@login_required
def contact_message_detail(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    return render(request, 'contact_messages/message_detail.html', {'message': message})


def is_manager_or_senior(user):
    return user.is_authenticated and user.employee_profile.role in ["manager", "senior"]


def create_travel_info(request):
    if request.method == 'POST':
        form = TravelInfoForm(request.POST, request.FILES)
        if form.is_valid():
            travel_info = form.save(commit=False)
            travel_info.save()  # Uloží TravelInfo včetně Assigned Employee
            return redirect('travel_info_list')  # Přesměrování po úspěchu
        else:
            messages.error(request, "Formulář obsahuje chyby. Zkontrolujte vstupy.")
    else:
        form = TravelInfoForm()

    return render(request, 'create_travel_info.html', {'form': form})


@login_required
@user_passes_test(lambda user: user.employee_profile.role in ['manager', 'senior'])
def travel_info_list(request):
    if request.method == "GET":
        travel_infos = TravelInfo.objects.all()
        return render(request, "travel_info_list.html", {
            "travel_infos": travel_infos
        })


@login_required
def delete_travel_info(request, travel_id):
    if request.user.employee_profile.role not in ["manager", "senior"]:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect("travel_info_list")

    travel_info = get_object_or_404(TravelInfo, id=travel_id)
    if request.method == "POST":
        travel_info.delete()
        messages.success(request, "Travel info deleted successfully!")
        return redirect("travel_info_list")

    return render(request, "confirm_delete.html", {"travel_info": travel_info})


@login_required
def assigned_trips(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    assigned_trips = TravelInfo.objects.filter(assigned_to=employee)
    return render(request, 'assigned_trips.html', {
        'employee': employee,
        'assigned_trips': assigned_trips,
    })


def role_check(user):
    if not hasattr(user, 'employee_profile'):
        raise PermissionDenied
    return True


@login_required
@user_passes_test(role_check)
def contact_message_list(request):
    messages1 = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'contact_messages/message_list.html', {'messages': messages1 })


@login_required
@user_passes_test(lambda user: user.employee_profile.role in ['manager', 'senior'])
def update_travel_info(request, travel_id):
    travel_info = get_object_or_404(TravelInfo, id=travel_id)

    if request.method == 'POST':
        form = TravelInfoForm(request.POST, instance=travel_info)
        if form.is_valid():
            form.save()
            return redirect('travel_info_list')  # Nebo jiná URL
    else:
        form = TravelInfoForm(instance=travel_info)

    return render(request, 'update_travel_info.html', {'form': form})