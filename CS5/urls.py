from django.contrib import admin
from django.urls import path
from viewer.admin import custom_admin_site
from viewer.views import all_trips, home

urlpatterns = [
    path('admin/', custom_admin_site.urls),

    path('', home ,name='home'),
    path('trips/', all_trips, name='all_trips'),


]
