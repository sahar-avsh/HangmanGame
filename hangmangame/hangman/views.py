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

from .forms import HangmanGameModelForm
from .models import HangmanGame, HangmanWord

from random import randint

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

class StartGameView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    template_name = 'hangman/start_game.html'
    model = HangmanGame
    form_class = HangmanGameModelForm

    def post(self, *args, **kwargs):
        self.object = None
        return super().post(self.request, *args, **kwargs)

    def form_valid(self, form):
        if form.cleaned_data['word_source'] == 'D':
            count = HangmanWord.objects.filter(difficulty=form.cleaned_data['word_difficulty']).count()
            word = HangmanWord.objects.filter(difficulty=form.cleaned_data['word_difficulty'])[randint(0, count - 1)]
            form.instance.guess_word = word
        return super().form_valid(form)

class GameDetailView(LoginRequiredMixin, DetailView):
    template_name = 'hangman/game_detail.html'
    model = HangmanGame

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(HangmanGame, id=id_)