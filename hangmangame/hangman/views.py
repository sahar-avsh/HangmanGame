from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
    View
)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

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

class MainView(TemplateView):
    template_name = 'hangman/main_page.html'