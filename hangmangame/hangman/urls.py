from django.urls import path

from .views import (
  GameDetailView,
  MainView,
  StartGameView,
)

app_name = 'hangman'
urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('start-game/', StartGameView.as_view(), name='start_game'),
    path('<int:id>/hanging/', GameDetailView.as_view(), name='game_detail'),
]