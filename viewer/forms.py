from django import forms
from django.contrib.auth.models import User

from .models import Employee, TourPurchase, TravelInfo, ContactMessage
from django import forms
from viewer.models import Employee
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('Manager', 'Manager'),
    ('Senior', 'Senior'),
    ('Customer Service', 'Customer Service'),
]


class EmployeeForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Employee
        fields = ['username', 'password', 'first_name', 'last_name', 'role', 'email', 'phone', 'assigned_trips']

    def save(self, commit=True):
        # Create user
        username = self.cleaned_data.pop('username')
        password = self.cleaned_data.pop('password')
        user = User.objects.create_user(username=username, password=password)

        # Create employee
        employee = super().save(commit=False)
        employee.user = user  # Associate the user with the employee
        if commit:
            user.save()
            employee.save()
            self.save_m2m()  # Save ManyToMany relationships
        return employee


class OrderForm(forms.ModelForm):
    class Meta:
        model = TourPurchase
        fields = [
            'adult_count',
            'child_count',
            'customer_name',
            'customer_email',
            'customer_phone',
            'customer_address',
            'special_requests',
            'payment_method',
            'order_status',  # Důležité pro úpravu stavu
            'travel_preferences',
        ]
        widgets = {
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class TravelInfoForm(forms.ModelForm):
    class Meta:
        model = TravelInfo
        fields = [
            'tour_name',
            'departure_city',
            'destination_city',
            'departure_date',
            'return_date',
            'price_per_adult',
            'price_per_child',
            'meal_type',
            'assigned_to',
            'description',
            'image',
        ]
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['status', 'assigned_to', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }