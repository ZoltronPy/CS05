from django.contrib import admin
from django.urls import path
from viewer import views
from viewer.admin import custom_admin_site

urlpatterns = (
    path('admin/', admin.site.urls),
    path('custom-admin/', custom_admin_site.urls),
    # Správná cesta pro Django admin panel
    path('', views.homepage, name='homepage'),  # Domovská stránka
    path('trips/', views.trip_list, name='trip_list'),  # Seznam zájezdů
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),  # Detail konkrétního zájezdu
    path('trip/<int:trip_id>/purchase/', views.purchase_trip, name='purchase_trip'))