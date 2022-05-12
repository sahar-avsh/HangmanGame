from django.shortcuts import render, get_object_or_404, redirect
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

from django.views.generic.base import ContextMixin
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
import datetime
from profiles.models import Profile

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

    # def render_to_response(self, context, **response_kwargs):
    #     """ Allow AJAX requests to be handled more gracefully """
    #     if self.request.is_ajax():
    #         unfinished_games = HangmanGame.objects.filter(player=self.request.user.profile).filter(result__isnull=True)
    #         durations = [game.time_allowed for game in unfinished_games]
    #         return JsonResponse({'durations': durations}, status=200, content_type='application/json', **response_kwargs)
    #     else:
    #         return super().render_to_response(context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.is_ajax():
                # context = self.get_context_data()
                unfinished_games = HangmanGame.objects.filter(player=self.request.user.profile).filter(result__isnull=True)
                durations = [game.time_allowed.total_seconds() * 1000 if game.time_allowed is not None else None for game in unfinished_games]
                ids = [game.id for game in unfinished_games]
                # print(durations)
                # return render(request, self.template_name, context)
                return JsonResponse({'durations': durations, 'ids': ids}, status=200, content_type='application/json')
            else:
                context = self.get_context_data()
                return render(request, self.template_name, context)
        else:
            # context = self.get_context_data()
            return render(request, self.template_name, {})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            unfinished_games = HangmanGame.objects.filter(player=self.request.user.profile).filter(result__isnull=True).order_by('-updated_date')
            context['unfinished_games'] = unfinished_games
            statuses = [get_current_status(game.guessed_letters, game.guess_word) for game in unfinished_games]
            context['statuses'] = statuses
            ids = [game.id for game in unfinished_games]
            context['ids'] = ids
        except (Profile.DoesNotExist, AttributeError):
            pass
        return context

class StartGameView(LoginRequiredMixin, AjaxableResponseMixin, CreateView):
    template_name = 'hangman/start_game.html'
    model = HangmanGame
    form_class = HangmanGameModelForm

    def post(self, *args, **kwargs):
        self.object = None
        return super().post(self.request, *args, **kwargs)

    def form_valid(self, form):
        print(form.cleaned_data)
        if form.cleaned_data['word_source'] == 'D':
            count = HangmanWord.objects.filter(difficulty=form.cleaned_data['word_difficulty']).count()
            word = HangmanWord.objects.filter(difficulty=form.cleaned_data['word_difficulty'])[randint(0, count - 1)]
            form.instance.guess_word = word
        form.instance.player = self.request.user.profile
        return super().form_valid(form)

class MakeGuessAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        obj = HangmanGame.objects.get(id=request.POST.get('id'))
        letter_guessed = request.POST.get('letter')
        all_guessed_letters = obj.guessed_letters
        if letter_guessed not in all_guessed_letters:
            all_guessed_letters += letter_guessed
            guesses_remaining = update_guesses_remaining(obj.guesses_allowed, obj.guess_word, letter_guessed)

            obj.guessed_letters = all_guessed_letters
            obj.guesses_allowed = guesses_remaining
            obj.save()

            is_game_finished, is_won = is_finished(obj.guessed_letters, obj.guess_word, obj.guesses_allowed)
            if is_game_finished:
                if is_won:
                    obj.result = HangmanGame.WIN
                else:
                    obj.result = HangmanGame.LOSS
                obj.save()

            current_status = get_current_status(obj.guessed_letters, obj.guess_word)
            hit, miss = classify_guessed_letters(obj.guessed_letters, obj.guess_word)
            image = serve_correct_image(obj.guesses_allowed)

            return JsonResponse({
                'hits': hit,
                'misses': miss,
                'is_game_finished': is_game_finished,
                'current_status': current_status,
                'guesses_remaining': guesses_remaining,
                'image': image
            }, status=200, content_type='application/json')
        else:
            return JsonResponse({'error': 'You already guessed this letter'}, status=400, content_type='application/json')

class UpdateTimeRemainingAjaxView(LoginRequiredMixin, View):
    # def post(self, request, *args, **kwargs):
    #     obj = HangmanGame.objects.get(id=request.POST.get('id'))
    #     time_remaining = request.POST.get('time_remaining')
    #     time_remaining_formatted = datetime.timedelta(milliseconds=int(time_remaining))
    #     obj.time_allowed = time_remaining_formatted
    #     obj.save()
    #     return JsonResponse({'saving': 'Done'}, status=200, content_type='application/json')
    def post(self, request, *args, **kwargs):
        # print(request.POST)
        for id_ in request.POST.keys():
            obj = HangmanGame.objects.get(id=int(id_))
            obj.time_allowed = datetime.timedelta(milliseconds=int(request.POST.get(id_)))
            obj.save()
        # for key, value in request.POST.items():
        #     obj = HangmanGame.objects.get(id=int(request.POST.getlist(key)))

        # object_list = [HangmanGame.objects.get(id=int(id_)) for id_ in request.POST.keys()]
        # time_remaining_list = []
        # for index, obj in enumerate(object_list):
        #     time_remaining_formatted = datetime.timedelta(milliseconds=int(time_remaining_list[index]))
        #     obj.time_allowed = time_remaining_formatted
        #     obj.save()
        return JsonResponse({'saving': 'Done'}, status=200, content_type='application/json')

class StatisticsDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'hangman/game_statistics.html'

    def calc_total_score(self, wins, losses):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wins = HangmanGame.objects.filter(player=self.request.user.profile).filter(result='W')
        losses = HangmanGame.objects.filter(player=self.request.user.profile).filter(result='L')
        context['wins'] = wins
        context['losses'] = losses
        context['wh'] = len([win for win in wins if win.get_guess_word_difficulty() == 'H'])
        context['wm'] = len([win for win in wins if win.get_guess_word_difficulty() == 'M'])
        context['we'] = len([win for win in wins if win.get_guess_word_difficulty() == 'E'])
        context['lh'] = len([loss for loss in losses if loss.get_guess_word_difficulty() == 'H'])
        context['lm'] = len([loss for loss in losses if loss.get_guess_word_difficulty() == 'M'])
        context['le'] = len([loss for loss in losses if loss.get_guess_word_difficulty() == 'E'])
        context['total'] = self.calc_total_score(wins, losses)
        return context

class GameDetailView(LoginRequiredMixin, DetailView):
    model = HangmanGame
    template_name = 'hangman/play_game.html'

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(HangmanGame, id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['current_status'] = get_current_status(obj.guessed_letters, obj.guess_word)
        context['available_letters'] = get_available_letters(obj.guessed_letters)
        hit, miss = classify_guessed_letters(obj.guessed_letters, obj.guess_word)
        context['hits'] = hit
        context['misses'] = miss
        context['is_finished'] = is_finished(obj.guessed_letters, obj.guess_word, obj.guesses_allowed)
        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.result or request.user.profile != obj.player:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


# class GameUpdateView(LoginRequiredMixin, UpdateView):
#     template_name = 'hangman/play_game.html'
#     model = HangmanGame
#     fields = ['guessed_letters']

#     def get_object(self):
#         id_ = self.kwargs.get('id')
#         return get_object_or_404(HangmanGame, id=id_)

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()

#         if request.GET.get('time_remaining'):
#             time_remaining = request.GET.get('time_remaining')
#             time_remaining_formatted = datetime.timedelta(milliseconds=int(time_remaining))
#             HangmanGame.objects.filter(id=self.object.id).update(time_allowed=time_remaining_formatted)

#         if request.GET.get('letter'):
#             letter_guessed = request.GET.get('letter')
#             all_guessed_letters = self.object.guessed_letters
#             if letter_guessed not in all_guessed_letters:
#                 all_guessed_letters += letter_guessed
#                 HangmanGame.objects.filter(id=self.object.id).update(guessed_letters=all_guessed_letters)
#                 guesses_remaining = update_guesses_remaining(self.object.guesses_allowed, self.object.guess_word, letter_guessed)
#                 HangmanGame.objects.filter(id=self.object.id).update(guesses_allowed=guesses_remaining)

#                 is_game_finished, is_won = is_finished(all_guessed_letters, self.object.guess_word, guesses_remaining)
#                 if is_game_finished and is_won:
#                     HangmanGame.objects.filter(id=self.object.id).update(result=HangmanGame.WIN)
#                 elif is_game_finished and not is_won:
#                     HangmanGame.objects.filter(id=self.object.id).update(result=HangmanGame.LOSS)

#                 current_status = get_current_status(all_guessed_letters, self.object.guess_word)
#                 hit, miss = classify_guessed_letters(all_guessed_letters, self.object.guess_word)

#                 image = serve_correct_image(guesses_remaining)

#                 return JsonResponse({
#                     'hits': hit,
#                     'misses': miss,
#                     'is_game_finished': is_game_finished,
#                     'current_status': current_status,
#                     'guesses_remaining': guesses_remaining,
#                     'image': image
#                 }, status=200, content_type='application/json')
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['available_letters'] = string.ascii_lowercase
#         context['current_status'] = get_current_status(self.object.guessed_letters, self.object.guess_word)
#         context['available_letters'] = get_available_letters(self.object.guessed_letters)
#         hit, miss = classify_guessed_letters(self.object.guessed_letters, self.object.guess_word)
#         context['hits'] = hit
#         context['misses'] = miss
#         context['is_finished'] = is_finished(self.object.guessed_letters, self.object.guess_word, self.object.guesses_allowed)
#         return context

#     def dispatch(self, request, *args, **kwargs):
#         obj = self.get_object()
#         if obj.result:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)

class GameFinishedView(LoginRequiredMixin, ContextMixin, View):
    template_name = 'hangman/game_finished.html'

    # def get_object(self):
    #     id_ = self.kwargs.get('id')
    #     return get_object_or_404(HangmanGame, id=id_)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        res = request.POST.get('lost')
        game = HangmanGame.objects.get(id=self.kwargs.get('id'))
        game.result = res
        game.save()
        # super().post(self, request, *args, **kwargs)
        return JsonResponse({'game': 'lost'}, status=200, content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # game = self.get_object()
        game = HangmanGame.objects.get(id=self.kwargs.get('id'))
        context['object'] = game
        if game.result == 'W':
            context['result'] = True
        else:
            context['result'] = False
        return context