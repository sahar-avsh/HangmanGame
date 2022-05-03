from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponse
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

from django.core.exceptions import PermissionDenied

from .forms import HangmanGameModelForm
from .models import HangmanGame, HangmanWord
from .utils import (
    get_current_status,
    is_finished, 
    get_available_letters, 
    classify_guessed_letters, 
    update_guesses_remaining,
    serve_correct_image
)

from random import randint
import string

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
                'url': reverse('hangman:play_game', kwargs={'id': self.object.id})
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

class GameUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'hangman/play_game.html'
    model = HangmanGame
    fields = ['guessed_letters']

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(HangmanGame, id=id_)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.GET.get('letter'):
            letter_guessed = request.GET.get('letter')
            all_guessed_letters = self.object.guessed_letters
            if letter_guessed not in all_guessed_letters:
                all_guessed_letters += letter_guessed
                HangmanGame.objects.filter(id=self.object.id).update(guessed_letters=all_guessed_letters)
                guesses_remaining = update_guesses_remaining(self.object.guesses_allowed, self.object.guess_word, letter_guessed)
                HangmanGame.objects.filter(id=self.object.id).update(guesses_allowed=guesses_remaining)

                is_game_finished, is_won = is_finished(all_guessed_letters, self.object.guess_word, guesses_remaining)
                if is_game_finished and is_won:
                    HangmanGame.objects.filter(id=self.object.id).update(result=HangmanGame.WIN)
                elif is_game_finished and not is_won:
                    HangmanGame.objects.filter(id=self.object.id).update(result=HangmanGame.LOSS)

                current_status = get_current_status(all_guessed_letters, self.object.guess_word)
                hit, miss = classify_guessed_letters(all_guessed_letters, self.object.guess_word)

                image = serve_correct_image(guesses_remaining)

                return JsonResponse({
                    'hits': hit,
                    'misses': miss,
                    'is_game_finished': is_game_finished,
                    'current_status': current_status,
                    'guesses_remaining': guesses_remaining,
                    'image': image
                }, status=200, content_type='application/json')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['available_letters'] = string.ascii_lowercase
        context['current_status'] = get_current_status(self.object.guessed_letters, self.object.guess_word)
        context['available_letters'] = get_available_letters(self.object.guessed_letters)
        hit, miss = classify_guessed_letters(self.object.guessed_letters, self.object.guess_word)
        context['hits'] = hit
        context['misses'] = miss
        context['is_finished'] = is_finished(self.object.guessed_letters, self.object.guess_word, self.object.guesses_allowed)
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.result:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class GameFinishedView(LoginRequiredMixin, TemplateView):
    template_name = 'hangman/game_finished.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_ = self.kwargs.get('id')
        game = HangmanGame.objects.get(id=id_)
        context['object'] = game
        if game.result == 'W':
            context['result'] = True
        else:
            context['result'] = False
        return context