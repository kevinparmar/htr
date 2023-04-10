from spellchecker import SpellChecker
from textblob import TextBlob
import nltk

def correct_spelling_pyspellchecker(text):
    # create a SpellChecker object
    spell = SpellChecker()
    
    # split the text into individual words
    words = text.strip().split(' ')

    # create an empty list to store the corrected words
    corrected_words = []

    # iterate through each word and correct any spelling errors
    for word in words:
        # get the corrected spelling of the word
        corrected_word = spell.correction(word)
        if corrected_word is None:
            blob = TextBlob(word)
            corrected_word = str(blob.correct())

        # add the corrected word to the list of corrected words
        corrected_words.append(corrected_word)

    # join the corrected words back into a string
    corrected_text = ' '.join(corrected_words)

    return corrected_text
 


def correct_spelling_textblob(text):
    # create a TextBlob object from the input text
    blob = TextBlob(text)

    # get a list of words in the text
    words = blob.words

    # create an empty list to store the corrected words
    corrected_words = []

    # iterate through each word and correct any spelling errors
    for word in words:
        # get the corrected spelling of the word
        corrected_word = str(word.correct())

        # add the corrected word to the list of corrected words
        corrected_words.append(corrected_word)

    # join the corrected words back into a string
    corrected_text = ' '.join(corrected_words)

    return corrected_text

import enchant

def correct_spelling_enchant(text):
    # create an Enchant dictionary object for English
    d = enchant.Dict("en_US")

    # split the text into individual words
    words = text.strip().split(' ')

    # create an empty list to store the corrected words
    corrected_words = []

    # iterate through each word and correct any spelling errors
    for word in words:
        # check if the word is spelled correctly
        if not d.check(word):
            # get a list of possible correct spellings
            suggestions = d.suggest(word)

            # if there are suggestions, take the first one
            if suggestions:
                corrected_word = suggestions[0]
            else:
                corrected_word = word  # if no suggestions, keep the original word
        else:
            corrected_word = word  # if spelled correctly, keep the original word

        # add the corrected word to the list of corrected words
        corrected_words.append(corrected_word)

    # join the corrected words back into a string
    corrected_text = ' '.join(corrected_words)

    return corrected_text
