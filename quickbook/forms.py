from django import forms
from django.utils.timezone import now
from .models import Booking


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
        facility = cleaned_data.get('facility')
        booking_date = cleaned_data.get('date')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        if facility and booking_date and start_time and end_time:
            overlapping_bookings = Booking.objects.filter(
                facility=facility,
                date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if self.instance:
                overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)

            facility_capacity = facility.capacity

            if overlapping_bookings.count() >= facility_capacity:
                raise forms.ValidationError(
                    f"The facility is already fully booked for this time slot. Capacity is {facility_capacity}.")

        return cleaned_data
