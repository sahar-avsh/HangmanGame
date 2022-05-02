import string

def is_finished(guessed_letters, word):
    return set(word).issubset(set(guessed_letters))

def get_current_status(guessed_letters, word):
    status = ''
    for letter in word:
        if letter in guessed_letters:
            status += letter
        else:
            status += ' __ '
    return status

def get_available_letters(guessed_letters):
    all_letters = string.ascii_lowercase
    return [letter for letter in all_letters if letter not in guessed_letters]

def classify_guessed_letters(guessed_letters, word):
    hit, miss = [], []
    for letter in guessed_letters:
        if letter in word:
            hit.append(letter)
        else:
            miss.append(letter)
    return hit, miss