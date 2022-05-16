import os
from time import perf_counter_ns
from syllables import closest_word

words = "words"


path = os.getcwd() + "/";

ENGLISH = "languages/english/"

english = {"words":set()}

with open(path + ENGLISH + words) as f:
    english[words] = set(f.read().split("\n"))

    
word = "splendide"

start = perf_counter_ns()

print(closest_word(word, english[words]))

print((perf_counter_ns() - start)/1_000_000_000)

