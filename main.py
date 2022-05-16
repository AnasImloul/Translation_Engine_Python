import os
from autocorrect import english_dictionary, correct
from time import perf_counter_ns
from syllables import closest_word

words = "words"

english = english_dictionary()

sentence = "i hav such a botifol viow from my chambre"

start = perf_counter_ns()

print(correct(sentence, english[words]))

print((perf_counter_ns() - start)/1_000_000_000)

