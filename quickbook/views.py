from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .forms import BookingForm
from .models import Facility, Booking
from .utils import available_slots
from .tasks import notify_on_facility_booking


class FacilitiesView(LoginRequiredMixin, ListView):
    """
        Retreives all the facilities available in the booking system.
    """
    model = Facility
    template_name = 'quickbook/facilities/list.html'
    context_object_name = 'facilities'
    ordering = ['name']


class AvailableSlotsView(LoginRequiredMixin, View):
    """
        Retrieves available slots on a particular date for the choosen facility.
    """
    def get(self, request, pk):
        facility = get_object_or_404(Facility, id=pk)
        date_str = request.GET.get('date')
        date = timezone.datetime.strptime(
            date_str, '%Y-%m-%d').date() if date_str else timezone.localdate()
        return JsonResponse(
            {'success': True, 'slots': available_slots(facility, date)})


class BookingsView(LoginRequiredMixin, ListView):
    """
        Retrieves all the bookings made by the User.
    """
    model = Booking
    template_name = 'quickbook/bookings/list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user).order_by(
            '-date', '-start_time')


class BookingBaseView(LoginRequiredMixin, View):
    """
        Base class for Booking - CREATE & UPDATE.
    """
    model = Booking
    form_class = BookingForm
    success_url = reverse_lazy('quickbook:bookings-list')

    def json_response(self, success, **kwargs):
        return JsonResponse({'success': success, **kwargs})


class BookingCreateView(BookingBaseView, CreateView):
    """
        Creates booking with respect to facility provided and
        associates with the user.
    """
    template_name = 'quickbook/bookings/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        booking = form.save()
        notify_on_facility_booking.delay(booking.id)
        return self.json_response(True, redirect_url=self.success_url)

    def form_invalid(self, form):
        return self.json_response(False, errors=form.errors)


class BookingUpdateView(BookingBaseView, UpdateView):
    """
        Updates booking.
    """
    template_name = 'quickbook/bookings/update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied(
                'You are not allowed to modify this booking.')
        return obj

    def form_invalid(self, form):
        return self.json_response(
            False,
            errors={
                field: list(errors) for field,
                errors in form.errors.items()})

    def form_valid(self, form):
        booking = form.save()
        return self.json_response(
            True,
            redirect_url=str(self.success_url),
            booking={
                'id': booking.id,
                'facility': booking.facility.name,
                'date': booking.date.strftime('%Y-%m-%d'),
                'start_time': booking.start_time.strftime('%H:%M'),
                'end_time': booking.end_time.strftime('%H:%M'),
                'status': booking.status,
            }
        )
