from django import forms

from .models import User
from .validator import Validator


class UserSignupForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'First Name'}))
    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.widgets.TextInput(
            attrs={
                'placeholder': 'Last Name'}))
    email = forms.EmailField(
        required=True,
        max_length=200,
        widget=forms.widgets.EmailInput(
            attrs={
                'placeholder': 'Email'}),
        validators=[
            Validator.unique_email_validator])
    password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput,
        validators=[
            Validator.password_validator])
    confirm_password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self):
        user = User.objects.create_user(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=200,
        widget=forms.widgets.EmailInput(
            attrs={
                'placeholder': 'Email'}))
    password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
