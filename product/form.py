from django import forms
from .models import ContactMsg


class ContactMsgForm(forms.ModelForm):
    class Meta:
        model =ContactMsg
        fields = '__all__'