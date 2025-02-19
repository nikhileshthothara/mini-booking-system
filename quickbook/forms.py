from django import forms
from .models import Facility, Booking


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'location', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facility Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Capacity'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['facility', 'date', 'start_time', 'end_time', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
