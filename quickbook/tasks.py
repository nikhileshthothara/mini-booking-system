from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from myproject.celery import app as celery_app
from .models import Booking

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta


@celery_app.task()
def auto_cancel_booking(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        if booking.status == "pending":
            booking.status = "cancelled"
            booking.save()
            send_mail(
                subject="Facility Booking Cancellation",
                message=f"Dear {booking.user.first_name},\n\nYour booking for {booking.facility.name} on {booking.date} at {booking.start_time} has been cancelled.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    booking.user.email],
                fail_silently=True,
            )
    except Booking.DoesNotExist:
        pass


def calculate_time_until_check(booking):
    tz = ZoneInfo(settings.LOCAL_TIMEZONE)
    current_datetime = datetime.now(tz)
    booking_start_datetime = timezone.make_aware(
        datetime.combine(booking.date, booking.start_time), tz)
    time_until_check = (booking_start_datetime - current_datetime -
                        timedelta(minutes=30)).total_seconds() / 60
    return max(0, time_until_check)


@celery_app.task()
def notify_on_facility_booking(booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        send_mail(
            subject="Facility Booking Notification",
            message=f"Dear {booking.user.username},\n\nYour booking for {booking.facility.name} on {booking.date} at {booking.start_time} is Booked.\n\nPlease confirm (If not) your booking prior to 30 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                booking.user.email],
            fail_silently=True,
        )
        if booking.status == "pending":
            time_until_check = calculate_time_until_check(booking)
            _ = auto_cancel_booking.apply_async(
                (booking_id,), countdown=time_until_check * 60)

    except Booking.DoesNotExist:
        pass
