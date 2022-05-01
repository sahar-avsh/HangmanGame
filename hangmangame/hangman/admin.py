from django.contrib import admin
from .models import HangmanWord, HangmanGame

# Register your models here.
admin.site.register([HangmanWord, HangmanGame])