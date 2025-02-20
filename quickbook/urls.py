from django.urls import path, re_path
from .views import FacilitiesView, AvailableSlotsView, BookingsView, BookingCreateView, BookingUpdateView

app_name = 'quickbook'

urlpatterns = [
    # NOTE: Allowing both '/' as well as '/bookings/' on this view.
    re_path(r'^(bookings/)?$', BookingsView.as_view(), name='bookings-list'),
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='bookings-update'),
    path('bookings/create/', BookingCreateView.as_view(), name='bookings-create'),
    path('facilities/', FacilitiesView.as_view(), name='facilities-list'),
    path('facilities/<int:pk>/', AvailableSlotsView.as_view(), name='facilities-slots'),
]