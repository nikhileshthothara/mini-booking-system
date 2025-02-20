from django.urls import path
from .views import FacilitiesView, AvailableSlotsView, BookingsView, BookingCreateView, BookingUpdateView

app_name = 'quickbook'

urlpatterns = [
    path('facilities/', FacilitiesView.as_view(), name='facilities-list'),
    path('facilities/<int:pk>/', AvailableSlotsView.as_view(), name='facilities-slots'),
    path('bookings/', BookingsView.as_view(), name='bookings-list'),
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='bookings-update'),
    path('bookings/create/', BookingCreateView.as_view(), name='bookings-create'),
]