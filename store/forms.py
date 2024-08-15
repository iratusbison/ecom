# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class StaffLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

from django import forms
from store.models.address import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'phone', 'city', 'state', 'postal_code', 'country']
