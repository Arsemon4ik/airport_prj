from .models import Passenger, Booking, Baggage
from django import forms
from django.forms import modelformset_factory


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'email', 'phone']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['passenger', 'flight', 'seat_class']
        widgets = {
            'passenger': forms.Select(attrs={'class': 'form-control'}),
            'flight': forms.Select(attrs={'class': 'form-control'}),
            'seat_class': forms.Select(attrs={'class': 'form-control'}),
        }


class BaggageForm(forms.ModelForm):
    class Meta:
        model = Baggage
        fields = ['total_weight', 'baggage_type', 'additional_baggage_fee']
        widgets = {
            'total_weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'baggage_type': forms.Select(attrs={'class': 'form-control'}),
            'additional_baggage_fee': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# FormSet для багажу
BaggageFormSet = modelformset_factory(
        Baggage,
        fields=('total_weight', 'baggage_type', 'additional_baggage_fee'),
        extra=1,  # Додаткові форми для багажу
        can_delete=True  # Можливість видалення
    )