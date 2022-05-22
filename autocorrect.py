import os
from Syllables import closest_word as close1
import json

words = "words.json"

path = os.getcwd() + "/";

ENGLISH = "languages/english/"

english = {words:set()}


def english_dictionary():
    with open(path + ENGLISH + words, 'r') as in_file:
        try:
            data = json.loads(in_file.read())
        except json.JSONDecodeError:
            data = dict()


    english[words] = data
    return english


def closest(word, dictionary):
    closest1 = close1(word, dictionary)
    return closest1

def correct(sentence, dictionary):
    words = sentence.split()

    for i in range(len(words)):
        words[i] = closest(words[i], dictionary)

    return " ".join(words)
