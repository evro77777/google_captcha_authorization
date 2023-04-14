from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    username = forms.EmailField(max_length=254, required=True,
                                widget=forms.TextInput(attrs={'placeholder': '*Email..'}))
    password1 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'password'}))
    password2 = forms.CharField(max_length=30, required=True,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Confirm password', 'class': 'password'}))

    token = forms.CharField(widget=forms.HiddenInput())

    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class AuthForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'password'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    town = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Town'}))
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    post_code = forms.CharField(max_length=8, required=True, widget=forms.TextInput(attrs={'placeholder': 'Post code'}))

    class Meta:
        model = UserProfile
        fields = ['address', 'town', 'country', 'post_code']
