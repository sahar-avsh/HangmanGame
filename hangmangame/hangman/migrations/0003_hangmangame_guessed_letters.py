# Generated by Django 3.2.13 on 2022-05-02 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hangman', '0002_auto_20220501_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='hangmangame',
            name='guessed_letters',
            field=models.CharField(default='', max_length=24),
        ),
    ]