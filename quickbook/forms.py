from django import forms
from django.utils.timezone import now
from .models import Facility, Booking


class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'location', 'capacity']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Facility Name'}),
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Location'}),
            'capacity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Total Capacity'}),
        }

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity < 1:
            raise forms.ValidationError("Capacity must be at least 1.")
        return capacity


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['facility', 'date', 'start_time', 'end_time', 'status']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'}),
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'}),
            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                            'class': 'form-control'}),
            'status': forms.Select(
                attrs={
                    'class': 'form-control'}),
        }

    def clean_date(self):
        booking_date = self.cleaned_data.get('date')
        if booking_date < now().date():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
        return cleaned_data
