from myproject.celery import app as celery_app

@celery_app.task()
def notify_on_booking_confirmation(booking_id):
    print("------Booking Confirmed------{}".format(booking_id))
