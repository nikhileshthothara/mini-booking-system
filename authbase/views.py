from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.views.generic import FormView

from .forms import UserSignupForm, UserLoginForm


class UserSignupView(FormView):
    """
        User signup or register view
        @params: first_name, last_name, email, password, confirm_password
    """
    template_name = 'authbase/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('quickbook:bookings-list')

    def form_valid(self, form):
        user = form.save()
        # MODIFY: Instead of logging in immediately, a 2 factor auth can be added
        #         like sending and email with a code etc and serve it using VerifyUser View.
        login(self.request, user)
        return JsonResponse(
            {'success': True, 'redirect_url': str(self.success_url)})

    def form_invalid(self, form):
        errors = {
            field: [
                str(error) for error in form.errors[field]] for field in form.errors}
        return JsonResponse({'success': False, 'errors': errors})


class UserLoginView(LoginView):
    """
        User login view
        @params: email, password
    """
    template_name = 'authbase/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('quickbook:bookings-list')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)

        if user:
            login(self.request, user)
            return JsonResponse(
                {'success': True, 'redirect_url': str(self.success_url)})
        else:
            return JsonResponse({'success': False, 'errors': 'User with email doesnt exist.'})
    
    def form_invalid(self, form):
        errors = {
            field: [
                str(error) for error in form.errors[field]] for field in form.errors}
        return JsonResponse({'success': False, 'errors': errors})
