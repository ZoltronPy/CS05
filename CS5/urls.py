from django.contrib import admin
from django.urls import path
from viewer.admin import custom_admin_site
from viewer.views import all_trips

urlpatterns = [
    path('admin/', custom_admin_site.urls),

    path('trips/', all_trips)


]
