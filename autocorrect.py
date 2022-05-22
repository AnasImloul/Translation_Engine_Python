import os
from Syllables import closest_word as sound_closest,distance as sound_distance
from typos import closest_word as typo_closest
import json

words = "words.json"

path = os.getcwd() + "/"

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




def correct(sentence, dictionary):
    words = (sentence.lower()).split()

    for i in range(len(words)):
        typo_correct = typo_closest(words[i], dictionary)

        if sound_distance(typo_correct, words[i]) < len(words[i]):
            words[i] = typo_correct
            continue

        sound_correct = sound_closest(words[i], dictionary)

        if sound_closest(sound_correct, words[i]) < sound_closest(typo_correct, words[i]):
            words[i] = sound_correct
        else:
            words[i] = typo_correct


    return " ".join(words)
