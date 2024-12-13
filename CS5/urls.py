from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import SubmittableLoginView, user_logout
from accounts.views import SignUpView
from viewer import views
from viewer.admin import custom_admin_site
from viewer.views import HotelsViewTemplateView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-admin/', custom_admin_site.urls),
    # Správná cesta pro Django admin panel
    path('', views.homepage, name='homepage'),  # Domovská stránka
    path('trips/', views.trip_list, name='trip_list'),  # Seznam zájezdů
    path('trip/<int:trip_id>/', views.trip_detail, name='trip_detail'),  # Detail konkrétního zájezdu
    path('trip/<int:trip_id>/purchase/', views.purchase_trip, name='purchase_trip'),
    path('contact/', views.contact, name='contact'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('hotels/', HotelsViewTemplateView.as_view(), name='hotels'),

    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),

    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', user_logout, name='logout'),


]