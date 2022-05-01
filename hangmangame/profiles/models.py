from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

# Create your models here.
class Profile(models.Model):
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.f_name + ' ' + self.l_name