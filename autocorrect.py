import os
from syllables import closest_word

words = "words"

path = os.getcwd() + "/";

ENGLISH = "languages/english/"

english = {"words":set()}

def english_dictionary():
    with open(path + ENGLISH + words) as f:
        english[words] = set(f.read().split("\n"))
    return english


def correct(sentence, dictionary):
    words = sentence.split()


    for i in range(len(words)):
        words[i] = closest_word(words[i], dictionary)

    return " ".join(words)