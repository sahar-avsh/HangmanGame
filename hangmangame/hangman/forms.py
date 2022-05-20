from django import forms

from .models import HangmanGame, HangmanWord

from .widgets import SplitDurationWidget

import re
class HangmanGameModelForm(forms.ModelForm):
    user_provided = 'U'
    db_provided = 'D'
    WORD_SOURCES = (
        (user_provided, 'USER'),
        (db_provided, 'RANDOM')
    )
    word_source = forms.ChoiceField(
        label='Word Source',
        initial=db_provided, 
        choices=WORD_SOURCES, 
        widget=forms.Select(),
        required=True
    )

    word_difficulty = forms.ChoiceField(
        label='Word Difficulty',
        initial=HangmanWord.easy,
        choices=HangmanWord.DIFFICULTY_CHOICES,
        widget=forms.Select(),
        required=False
    )
    class Meta:
        model = HangmanGame
        fields = [
            'guess_word',
            'time_allowed',
            'guesses_allowed'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['word_difficulty'].widget.attrs['id'] = 'id-word_difficulty_field'
        self.fields['word_difficulty'].widget.attrs['class'] = 'word_difficulty_field'
        self.fields['word_difficulty'].widget.attrs['name'] = 'word_difficulty'

        self.fields['word_source'].widget.attrs['id'] = 'id-word_source_field'
        self.fields['word_source'].widget.attrs['class'] = 'word_source_field'
        self.fields['word_source'].widget.attrs['name'] = 'word_source'

        self.fields['guess_word'].widget = forms.TextInput(attrs={
            'id': 'id-guess_word-field',
            'class': 'guess_word-field',
            'name': 'guess_word',
            'placeholder': 'Enter a word'})
        self.fields['guess_word'].required = False

        self.fields['time_allowed'].widget = SplitDurationWidget(attrs={
            'type': 'text',
            'id': 'id-time_allowed-field',
            'class': 'time_allowed-field',
            'name': 'time_allowed'})
        self.fields['time_allowed'].required = False
        self.fields['time_allowed'].help_text = 'Leave blank if unlimited'

        self.fields['guesses_allowed'].widget.attrs['id'] = 'id-guesses_allowed-field'
        self.fields['guesses_allowed'].widget.attrs['class'] = 'guesses_allowed-field'
        self.fields['guesses_allowed'].widget.attrs['name'] = 'guesses_allowed'
        self.fields['guesses_allowed'].widget.attrs['placeholder'] = 'Leave blank if unlimited'
        self.fields['guesses_allowed'].required = False
    
    def clean_guess_word(self):
        word = self.data.get('guess_word').lower()
        pattern = re.search("[^A-Za-z\s]", word)
        if pattern:
            raise forms.ValidationError("Word can only include ASCII characters.")

    def clean_time_allowed(self):
        h = self.data.get('time_allowed_hours') if self.data.get('time_allowed_hours') != '' else 0
        m = self.data.get('time_allowed_minutes') if self.data.get('time_allowed_minutes') != '' else 0
        s = self.data.get('time_allowed_seconds') if self.data.get('time_allowed_seconds') != '' else 0
        try:
            if any([int(i) < 0 for i in [h, m, s]]):
                raise forms.ValidationError("Duration cannot be negative.")
        except (ValueError):
            raise forms.ValidationError("Please input integers only.")
        return '{}:{}:{}'.format(h, m, s)
