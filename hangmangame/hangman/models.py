from django.db import models

# Create your models here.
class HangmanWord(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word