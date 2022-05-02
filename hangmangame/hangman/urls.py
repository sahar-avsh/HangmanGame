from django.urls import path

from .views import (
  GameUpdateView,
  MainView,
  StartGameView,
)

app_name = 'hangman'
urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('start-game/', StartGameView.as_view(), name='start_game'),
    path('<int:id>/hanging/', GameUpdateView.as_view(), name='play_game'),
]