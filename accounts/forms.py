from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {'username': 'Username',
                  'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Email',
                  'password1': 'PASSWORD',
                  'password2': 'PASSWORD CONFIRMATION'

                  }



