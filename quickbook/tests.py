from django.test import TestCase
from django.urls import reverse
from authbase.models import User
from quickbook.models import Booking, Facility


class BookingsViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser", password="password")
        self.client.login(email="testuser", password="password")
        self.facility = Facility.objects.create(
            name="Test Facility", location="Test Location", capacity=10)
        self.booking1 = Booking.objects.create(
            user=self.user,
            facility=self.facility,
            date="2025-02-20",
            start_time="10:00",
            end_time="11:00",
            status="confirmed")
        self.booking2 = Booking.objects.create(
            user=self.user,
            facility=self.facility,
            date="2025-02-21",
            start_time="12:00",
            end_time="13:00",
            status="confirmed")

    def test_bookings_view(self):
        response = self.client.get(reverse('quickbook:bookings-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quickbook/bookings/list.html')
        self.assertIn('bookings', response.context)
        self.assertEqual(len(response.context['bookings']), 2)

    def test_bookings_view_no_login(self):
        self.client.logout()
        response = self.client.get(reverse('quickbook:bookings-list'))
        self.assertRedirects(response, '/auth/login/?next=/')


class BookingCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser", password="password")
        self.client.login(email="testuser", password="password")
        self.facility = Facility.objects.create(
            name="Test Facility", location="Test Location", capacity=10)

    def test_booking_create_valid_form(self):
        data = {
            'facility': self.facility.id,
            'date': '2025-02-20',
            'start_time': '10:00',
            'end_time': '11:00',
            'status': 'confirmed'
        }
        response = self.client.post(reverse('quickbook:bookings-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             'success': True, 'redirect_url': '/'})
        self.assertTrue(Booking.objects.filter(user=self.user).exists())

    def test_booking_create_invalid_form(self):
        data = {
            'facility': '',
            'date': '',
            'start_time': '10:00',
            'end_time': '11:00',
            'status': 'confirmed'
        }
        response = self.client.post(reverse('quickbook:bookings-create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'success': False, 'errors': {
                             'facility': ['This field is required.'], 'date': ['This field is required.']}})


class BookingUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser", password="password")
        self.client.login(email="testuser", password="password")
        self.facility = Facility.objects.create(
            name="Test Facility", location="Test Location", capacity=10)
        self.booking = Booking.objects.create(
            user=self.user,
            facility=self.facility,
            date="2025-02-20",
            start_time="10:00",
            end_time="11:00",
            status="confirmed")

    def test_booking_update_valid_form(self):
        data = {
            'facility': self.facility.id,
            'date': '2025-02-20',
            'start_time': '10:00',
            'end_time': '11:00',
            'status': 'confirmed'
        }
        response = self.client.post(
            reverse(
                'quickbook:bookings-update',
                args=[
                    self.booking.id]),
            data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
            'success': True,
            'redirect_url': '/',
            'booking': {
                'id': self.booking.id,
                'facility': self.booking.facility.name,
                'date': '2025-02-20',
                'start_time': '10:00',
                'end_time': '11:00',
                'status': 'confirmed',
            }
        })
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.start_time.strftime('%H:%M'), '10:00')

    def test_booking_update_invalid_form(self):
        data = {
            'facility': '',
            'date': '',
            'start_time': '10:00',
            'end_time': '11:00',
            'status': 'confirmed'
        }
        response = self.client.post(
            reverse(
                'quickbook:bookings-update',
                args=[
                    self.booking.id]),
            data)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'success': False, 'errors': {
                             'facility': ['This field is required.'], 'date': ['This field is required.']}})

    def test_booking_update_permission_denied(self):
        _ = User.objects.create_user(email="testuser2", password="password")
        self.client.logout()
        self.client.login(email="testuser2", password="password")
        data = {
            'facility': self.facility.id,
            'date': '2025-02-20',
            'start_time': '10:00',
            'end_time': '11:00',
            'status': 'confirmed'
        }
        response = self.client.post(
            reverse(
                'quickbook:bookings-update',
                args=[
                    self.booking.id]),
            data)
        self.assertEqual(response.status_code, 403)


class OverlappingBookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser", password="password")
        self.client.login(email="testuser", password="password")
        self.facility = Facility.objects.create(
            name="Test Facility", location="Test Location", capacity=1)
        self.booking = Booking.objects.create(
            user=self.user,
            facility=self.facility,
            date="2025-02-20",
            start_time="10:00",
            end_time="11:00",
            status="confirmed"
        )

    def test_overlapping_bookings_validation(self):
        data = {
            'facility': self.facility.id,
            'date': '2025-02-20',
            'start_time': '10:00',
            'end_time': '11:00',
            'status': 'confirmed'
        }
        response = self.client.post(reverse('quickbook:bookings-create'), data)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertIn(
            "The facility is already fully booked for this time slot. Capacity is 1.",
            response['errors']['__all__'])
