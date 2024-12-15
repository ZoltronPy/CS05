from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from .forms import SignUpForm


class SubmittableLoginView(LoginView):
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log In'  # Nadpis
        context['button_text'] = 'Log In'  # Text tlačítka
        return context


class SignUpView(CreateView):
    template_name = 'form.html'
    form_class = SignUpForm
    success_url = reverse_lazy('homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'  # Nadpis
        context['button_text'] = 'Register'  # Text tlačítka
        return context


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

