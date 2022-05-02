from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class HangmanWord(models.Model):
    hard = 'H'
    medium = 'M'
    easy = 'E'
    DIFFICULTY_CHOICES = (
        (hard, 'HARD'),
        (medium, 'MEDIUM'),
        (easy, 'EASY')
    )

    word = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        self.difficulty = self.calc_word_difficulty()
        super().save(*args, **kwargs)

    def calc_word_difficulty(self):
        # calc word score
        score = len(self.word) + len(set(self.word))
        if score > 15:
            return self.hard
        elif score > 10:
            return self.medium
        else:
            return self.easy

class HangmanGame(models.Model):
    WIN = 'W'
    LOSS = 'L'
    RESULT_CHOICES = (
        (WIN, 'WON'),
        (LOSS, 'LOST')
    )
    guess_word = models.CharField(max_length=100)
    time_allowed = models.DurationField(null=True)
    guesses_allowed = models.IntegerField(default=7, validators=[
        MaxValueValidator(7),
        MinValueValidator(1)
    ])
    started_date = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=1, choices=RESULT_CHOICES, null=True)
    guessed_letters = models.CharField(max_length=26, default='')

    def __str__(self):
        return self.guess_word

    def get_absolute_url(self):
        return reverse('hangman:play_game', kwargs={'id': self.id})
    