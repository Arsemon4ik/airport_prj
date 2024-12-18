from .models import Passenger, Booking
from django import forms


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
        fields = ['passenger', 'flight', 'baggage', 'seat_class']
        widgets = {
            'passenger': forms.Select(attrs={'class': 'form-control'}),
            'flight': forms.Select(attrs={'class': 'form-control'}),
            'baggage': forms.Select(attrs={'class': 'form-control'}),
            'seat_class': forms.Select(attrs={'class': 'form-control'}),
        }
