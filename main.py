from autocorrect import english_dictionary, correct
from time import perf_counter_ns

words = "words"

english = english_dictionary()

sentence = "i hev sush botifol viow frome my roome"

start = perf_counter_ns()

print(correct(sentence, english[words]))

print((perf_counter_ns() - start)/1_000_000_000)
