from autocorrect import english_dictionary, correct
from time import perf_counter_ns

words = "words.json"

english = english_dictionary()

sentence = "i hab sach beotifl viow frum mi cambre"

start = perf_counter_ns()



print(correct(sentence, english[words]))



print((perf_counter_ns() - start)/1_000_000_000)

