from django import template
import string

register = template.Library()

BAD_WORDS = ['редиска', 'плохоеслово', 'мат']


@register.filter
def censor(value):
    if not isinstance(value, str):
        return value

    words = value.split()
    censored_words = []

    for word in words:

        clean_word = word.strip(string.punctuation).lower()

        if clean_word in BAD_WORDS:

            first_letter = word[0]
            replacement = first_letter + '*' * (len(word) - 1)
            censored_words.append(replacement)

        else:
            censored_words.append(word)

    return " ".join(censored_words)