from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from accounts.views import SubmittableLoginView, user_logout, SignUpView
from viewer import views
from viewer.admin import custom_admin_site

urlpatterns = [
    # Admin paths
    path('admin/', admin.site.urls),
    path('custom-admin/', custom_admin_site.urls),

    # Homepage and main sections
    path('', views.homepage, name='homepage'),
    path('trips/', views.trip_list, name='trip_list'),
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('trip/<int:trip_id>/purchase/', views.purchase_trip, name='purchase_trip'),
    path('contact/', views.contact, name='contact'),
    path('thank_you/', views.thank_you, name='thank_you'),

    # Hotels
    path('hotels/', views.hotels, name='hotels'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),

    # User accounts
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Offers and search
    path('offers/', views.all_offers, name='all_offers'),
    path('offers/<int:pk>/', views.offer_detail, name='offer_detail'),
    path('search/', views.search_results, name='search_results'),

    # Employees
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/<int:employee_id>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),

    # Orders
    path('orders/', views.order_list, name='order_list'),  # Seznam všech objednávek
    path('orders/employee/<int:employee_id>/', views.order_list, name='order_list_by_employee'),
    # Objednávky podle zaměstnance
    path('orders/add/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/delete/', views.order_delete, name='order_delete'),

    path('contact_messages/', views.contact_message_list, name='contact_message_list'),
    path('contact_messages/<int:message_id>/', views.contact_message_detail, name='contact_message_detail'),

    path('travel-info/', views.travel_info_list, name='travel_info_list'),
    path("create-tour/", views.create_travel_info, name="create_travel_info"),

    path("travel-info-list/", views.travel_info_list, name="travel_info_list"),
    path('travel-info/update/<int:travel_id>/', views.update_travel_info, name='update_travel_info'),
    path("travel-info/delete/<int:travel_id>/", views.delete_travel_info, name="delete_travel_info"),

    path('assigned-trips/<int:employee_id>/', views.assigned_trips, name='assigned_trips'),

    path('contact_messages/', views.contact_message_list, name='contact_message_list'),
    path('contact_messages/<int:message_id>/', views.contact_message_detail, name='contact_message_detail'),


    path('payment/<int:purchase_id>/', views.payment_process, name='payment_process'),
    path('purchase/success/<int:purchase_id>/', views.purchase_success, name='purchase_success'),

]



# Static and media files in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


