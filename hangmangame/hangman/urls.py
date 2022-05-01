from django.urls import path

from .views import (
  MainView,
)

app_name = 'hangman'
urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
]