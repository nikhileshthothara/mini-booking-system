from django.db import models
from authbase.models import User


class Facility(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    location = models.CharField(max_length=100, db_index=True)
    capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Facility: {self.name} ID: {self.id}'


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings")
    facility = models.ForeignKey(
        Facility,
        on_delete=models.CASCADE,
        related_name="bookings")
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('facility', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f'Booking ID: {self.id}'
