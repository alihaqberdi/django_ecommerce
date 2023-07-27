from django import forms
from .models import CustomUser


class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }











