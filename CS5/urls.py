from django.contrib import admin
from django.urls import path
from viewer.admin import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
]
