from django.contrib import admin
from django.urls import path, include
from viewer import views
from viewer.admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),  # Vlastní administrátorský panel
    path('', views.homepage, name='homepage'),  # Domovská stránka
    path('trips/', views.trip_list, name='trip_list'),  # Seznam zájezdů
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),  # Detail zájezdu
    path('purchase/', views.purchase_trip, name='purchase_trip'),  # Nákup zájezdu
]
