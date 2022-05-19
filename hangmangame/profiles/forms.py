from django import forms
from .models import (
  Profile
)

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth import login, authenticate

class UserRegisterForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

  def __init__(self, request, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.request = request

    self.fields['username'].widget = forms.TextInput(attrs={
        'id': 'username_field_register',
        'class': 'inputs',
        'name': 'username',
        'placeholder': 'Enter your username'})

    self.fields['email'].widget = forms.TextInput(attrs={
        'id': 'email_field_register',
        'class': 'inputs',
        'name': 'email',
        'placeholder': 'Enter your email'})

    self.fields['first_name'].widget = forms.TextInput(attrs={
        'id': 'first_name_field_register',
        'class': 'inputs',
        'name': 'first_name',
        'placeholder': 'Enter your first name'})

    self.fields['last_name'].widget = forms.TextInput(attrs={
        'id': 'last_name_field_register',
        'class': 'inputs',
        'name': 'last_name',
        'placeholder': 'Enter your last name'})

    self.fields['password1'].widget = forms.TextInput(attrs={
        'id': 'password1_field_register',
        'class': 'inputs',
        'name': 'password1',
        'placeholder': 'Enter your password',
        'type': 'password'})

    self.fields['password2'].widget = forms.TextInput(attrs={
        'id': 'password2_field_register',
        'class': 'inputs',
        'name': 'password2',
        'placeholder': 'Confirm your password',
        'type': 'password'})

  def save(self, commit=True):
    user = super().save(commit=commit)
    if commit:
        auth_user = authenticate(
            username=self.cleaned_data['username'], 
            password=self.cleaned_data['password1']
        )
        login(self.request, auth_user)

    return user

  def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')
    try:
      user = User.objects.get(email=email)
      self.add_error('email', "A profile with this email already exists.")
    except (User.DoesNotExist):
      return cleaned_data
class UserLoginForm(AuthenticationForm):
  class Meta:
    model = User
    fields = ['username', 'password']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget = forms.TextInput(attrs={
        'id': 'username_field',
        'class': 'inputs',
        'name': 'username',
        'placeholder': 'Enter your username'})

    self.fields['password'].widget = forms.TextInput(attrs={
        'id': 'password_field',
        'class': 'inputs',
        'name': 'password',
        'placeholder': 'Enter your password',
        'type': 'password'})

class ProfileModelForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = [
        'f_name',
        'l_name',
    ]

    labels = {
      'f_name': 'First name',
      'l_name': 'Last name',
    }