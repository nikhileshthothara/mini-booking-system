from datetime import datetime, timedelta
from django.utils import timezone


def available_slots(facility, date):
    """
        This utility function is to retrieve available slots with respect
        to the facility and date provided based on capacity.

        Assumptions:
          - All facilities are open 24 Hrs (If not necessary, MODIFY's are to be made.)
    """
    booked_slots = facility.bookings.filter(
        date=date).exclude(
        status='cancelled').values(
            'start_time',
        'end_time').distinct()
    booked_slots = sorted(
        [(booking['start_time'], booking['end_time']) for booking in booked_slots])
    
    # MODIFY: retrieve the opening time and closing time of facility from DB.
    start_of_day = timezone.make_aware(
        datetime.combine(date, datetime.min.time()))
    end_of_day = start_of_day + timedelta(days=1)

    all_slots = []
    current_time = start_of_day

    for booked_start, booked_end in booked_slots:
        booked_start_datetime = timezone.make_aware(
            datetime.combine(date, booked_start))
        booked_end_datetime = timezone.make_aware(
            datetime.combine(date, booked_end))

        if current_time < booked_start_datetime:
            all_slots.append((current_time, booked_start_datetime))

        all_slots.append((booked_start_datetime, booked_end_datetime))

        current_time = max(current_time, booked_end_datetime)

    if current_time < end_of_day:
        all_slots.append((current_time, end_of_day))

    formatted_slots = []
    for slot in all_slots:
        slot_start, slot_end = slot

        # NOTE: checking the overlapping bookings
        booked_count = facility.bookings.filter(
            date=date,
            start_time__lt=slot_end.time(),
            end_time__gt=slot_start.time()
        ).exclude(status='cancelled').count()

        available_capacity = facility.capacity - booked_count
        if available_capacity > 0:
            formatted_slots.append({
                'start_time': slot_start.strftime('%I:%M %p'),
                'end_time': slot_end.strftime('%I:%M %p'),
                'available_capacity': available_capacity
            })
    return formatted_slots
