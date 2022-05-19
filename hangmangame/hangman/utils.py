import string

def is_finished(guessed_letters, word, guesses_remaining):
    is_guessed = set(word.lower().replace(' ', '')).issubset(set(guessed_letters.lower()))
    is_out_of_guesses = guesses_remaining == 0
    is_over = is_guessed or is_out_of_guesses
    return is_over, is_guessed

def get_current_status(guessed_letters, word):
    status = ''
    for letter in word.lower():
        if letter in guessed_letters.lower() or letter == ' ':
            status += letter
        else:
            status += '_'
    return status

def get_available_letters(guessed_letters):
    all_letters = string.ascii_lowercase
    return [letter for letter in all_letters if letter not in guessed_letters.lower()]

def classify_guessed_letters(guessed_letters, word):
    hit, miss = [], []
    for letter in guessed_letters.lower():
        if letter in word.lower():
            hit.append(letter)
        else:
            miss.append(letter)
    return hit, miss

def update_guesses_remaining(guesses_remaining, word, letter):
    if letter.lower() not in word.lower():
        guesses_remaining -= 1
    return guesses_remaining

def serve_correct_image(guesses_remaining):
    my_dict = {
        6: "1",
        5: "2",
        4: "3",
        3: "4",
        2: "5",
        1: "6",
        0: "7",
    }
    return my_dict[guesses_remaining]
