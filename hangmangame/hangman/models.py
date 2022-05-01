from django.db import models
from django.urls import reverse

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
        if score > 12:
            return self.hard
        elif score > 7:
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
    time_allowed = models.TimeField(null=True)
    guesses_allowed = models.IntegerField(null=True)
    started_date = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=1, choices=RESULT_CHOICES, null=True)

    def __str__(self):
        return self.guess_word

    def get_absolute_url(self):
        return reverse('hangman:game_detail', kwargs={'id': self.id})
    