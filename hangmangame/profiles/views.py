from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    PasswordResetView,
)

from django.contrib.auth import login, authenticate

from django.core.exceptions import PermissionDenied

from .models import (
  Profile,
)

from .forms import (
    ProfileModelForm,
    UserLoginForm,
    UserRegisterForm
)

# Create your views here.
class AjaxableResponseMixin(object):
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'id': self.object.id,
            }
            return JsonResponse(data)
        else:
            return response

class CustomLoginView(SuccessMessageMixin, FormView):
    template_name = 'profiles/login.html'
    form_class = UserLoginForm
    success_message = 'You have successfully logged in'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request=self.request, username=username, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'status': 'Wrong username or password'}, status=400)

    def get_success_url(self):
        return reverse_lazy('hangman:main_page')


class CustomSignUpView(SuccessMessageMixin, AjaxableResponseMixin, CreateView):
    template_name = 'profiles/register.html'
    form_class = UserRegisterForm
    success_message = 'Your profile was created successfully'
    success_url = reverse_lazy('hangman:main_page')

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(created_by=user, f_name=user.first_name, l_name=user.last_name)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return JsonResponse({'status': form.errors}, status=400)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs

class CustomResetPasswordView(SuccessMessageMixin, AjaxableResponseMixin, PasswordResetView):
    template_name = 'profiles/password_reset.html'
    email_template_name = 'profiles/password_reset_email.html'
    subject_template_name = 'profiles/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting up your password, " \
                      "if an account exists with the email you entered, you should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you had registered with, and check your spam folder."
    success_url = reverse_lazy('hangman:main_page')


class ProfileUpdateView(LoginRequiredMixin, AjaxableResponseMixin, UpdateView):
    template_name = 'profiles/profile_update.html'
    form_class = ProfileModelForm

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Profile, id=id_)

    def form_valid(self, form):
        data = form.cleaned_data
        self.object = form.save(commit=False)
        if data.get('clear_image'):
            self.object.image = None
        self.object.save()
        return JsonResponse({'update': 'done'}, status=200)

    def dispatch(self, request, *args, **kwargs):
        object = Profile.objects.get(id=self.kwargs.get('id'))
        if request.user.profile != object:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ProfileDetailView(LoginRequiredMixin, AjaxableResponseMixin, DetailView):
    template_name = 'profiles/profile_detail.html'
    model = Profile

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Profile, id=id_)