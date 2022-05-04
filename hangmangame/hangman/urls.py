from django.urls import path

from .views import (
  GameDetailView,
  MainView,
  StartGameView,
  GameFinishedView,
  MakeGuessAjaxView,
  UpdateTimeRemainingAjaxView,
  StatisticsDetailView
)

app_name = 'hangman'
urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('start-game/', StartGameView.as_view(), name='start_game'),
    path('<int:id>/hanging/', GameDetailView.as_view(), name='play_game'),
    path('ajax/make-guess/', MakeGuessAjaxView.as_view(), name='make_guess'),
    path('ajax/update-time-remaining/', UpdateTimeRemainingAjaxView.as_view(), name='update_time'),
    path('<int:id>/game-over/', GameFinishedView.as_view(), name='game_over'),
    path('stats/', StatisticsDetailView.as_view(), name='stats')
]