from autocorrect import english_dictionary, correct
from time import perf_counter

words = "words.json"

english = english_dictionary()

misspelled_sentence = "My trhee yera old duaghtre was trying to raost a marshmallow for teh first tiem Her fisrt adn seocnd attepmst ended in flmaes Both tiems I took the scochred marshmallow off of teh roatsign stikc and trhew it into the fire The tihrd tmie I helpde her a lot more adn together we achieved a perfectly tosaty golden borwn Ocne it was colo I handed her teh marshmallwo which seh promplty thrwe into teh fire No oen had tlod her seh was supposde to eat it Sbumitted by Luo Roses Parachute Cloroado Hree aer".lower()
correct_sentence = "My three year old daughter was trying to roast a marshmallow for the first time Her first and second attempts ended in flames Both times I took the scorched marshmallow off of the roasting stick and threw it into the fire The third time I helped her a lot more and together we achieved a perfectly toasty golden brown Once it was cool I handed her the marshmallow which she promptly threw into the fire No one had told her she was supposed to eat it Submitted by Lou Roess Parachute Colorado Here are more".lower()
start = perf_counter()


corrected = correct(misspelled_sentence, english[words])


correct_count = 0

for corrected_word,correct_word in zip(corrected.split(),correct_sentence.split()):
    correct_count += corrected_word==correct_word

print(f"correction precision : {round(correct_count/len(correct_sentence.split())*100,2)}%")
#correction precision : 92.63%


print(f"Auto-corrected a text containing {len(correct_sentence.split())} words in {(perf_counter() - start)} seconds.")
#Auto-corrected a text containing 95 words in 4.73588811099944 seconds.
