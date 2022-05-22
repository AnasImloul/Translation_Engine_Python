composite_consonants = {
                        "sh" : {"ch":1},
                        "ch" : {"sh":1},
                        "gh" : {"g" : 2},
                        "sc" : {"s":1,"sk" : 2},
                        "ph" : {"f" : 1},
                        "ck" : {"k" : 1, "q" : 1},
                        "ng" : {"n" : 1, "g" : 1},
                        "sk" : {"sc" : 2}
}

consonants = {
    'b' : {"p" : 2, "v" : 3},
    'c' : {},
    'd' : {},
    'f' : {},
    'g' : {},
    'h' : {},
    'j' : {},
    'k' : {},
    'l' : {},
    'm' : {},
    'n' : {},
    'p' : {},
    'q' : {"c" : 2, "k" : 3},
    'r' : {},
    's' : {"c":1,"z":2},
    't' : {},
    'v' : {},
    'w' : {},
    'x' : {},
    'y' : {},
    'z' : {"s":2}
}

vowels = {
    "a" : {"e":1,"i":1},
    "e" : {"a":1,"i":2,"":1},
    "i" : {"e":1,"a":1},
    "o" : {"u":1},
    "u":{"o":1, "a":2}
}

composite_vowels = {
                    "au" : {"o":1, "u":2},
                    "ou" : {"o":1, "u":2},
                    "ea" : {"e":1, "a":2,"i":3,"":1},
                    "ae" : {"e":1, "a":2,"i":3},
                    "oe" : {"e":1, "o" :2},
}



def current_vowel(word,i):

    if i < len(word) and word[i] in vowels:
        if i + 1 < len(word) and word[i:i+2] in composite_vowels:
            return word[i:i+2],i+2
        else:
            return word[i],i+1
    return "",i

def distance_vowels(vowel1, vowel2):

    if vowel1 == vowel2:
        return 0

    parents1 = {}
    parents2 = {}

    d = 8



    if vowel1 in composite_vowels:
        parents1 = composite_vowels[vowel1]

        if vowel2 in composite_vowels:
            parents2 = composite_vowels[vowel2]

            intersect = parents1.keys() & parents2.keys()


            for vowel in intersect:
                # use only one way distance since we want to check similarity to the dictionary and not the reversed direction
                d = min(d, parents1[vowel])# + parents2[vowel])

            return d

        elif vowel2 in vowels:
            d = parents1.get(vowel2,d)
            return d

    elif vowel1 in vowels:

        if vowel2 in composite_vowels:
            parents2 = composite_vowels[vowel2]

            if vowel1 in vowels:
                d = parents2.get(vowel1, d)
                return d
        elif vowel2 in vowels:
            #use only one way distance since we want to check similarity to the dictionary and not the reversed direction
            d = min(vowels[vowel2].get(vowel1, d), vowels[vowel1].get(vowel2, d))
            return d

    return d

def distance_all_vowels(vowel1, vowel2):
    i,j = 0,0

    n,m = len(vowel1), len(vowel2)

    d = 0

    while i<n or j<m:
        current1,i = current_vowel(vowel1,i)
        current2,j = current_vowel(vowel2,j)

        d += distance_vowels(current1,current2)
    return d

def current_consonant(word,i):
    if i < len(word) and word[i] not in vowels:
        if i + 1 < len(word) and word[i:i+2] in composite_consonants:
            return word[i:i+2],i+2
        else:
            return word[i],i+1
    return "",i

def distance_consonants(consonant1, consonant2):
    if consonant1 == consonant2:
        return 0

    parents1 = {}
    parents2 = {}

    d = 8

    if consonant1 in composite_consonants:
        parents1 = composite_consonants[consonant1]

        d = parents1.get(consonant2,d)

        if consonant2 in composite_consonants:
            parents2 = composite_consonants[consonant2]

            d = parents2.get(consonant1, d)

            return d

        elif consonant2 in consonants:
            d = parents1.get(consonant2,d)
            return d

    elif consonant1 in consonants:

        if consonant2 in composite_consonants:
            parents2 = composite_consonants[consonant2]

            if consonant1 in consonants:
                d = parents2.get(consonant1, d)
                return d
        elif consonant2 in consonants:
            #use only one way distance since we want to check similarity to the dictionary and not the reversed direction
            d = min((consonants[consonant1].get(consonant2, d) , consonants[consonant2].get(consonant1, d)))
            return d

    return d


def syllables(word):

    word = word.lower()

    if len(word) > 1 and word[-1] == "e":
        word = word[:-1]

    n = len(word)

    vowel_sound = False
    current,count = word[0],0

    i = 0

    _syllables_ = []

    syllable = ""


    while i < n:

        char = word[i]

        if current == char:
            if count >= 2:
                i += 1
                continue
            count += 1

        else:
            current = char
            count = 1


        if not char.isalpha():
            i += 1
            continue

        # if current character is a vowel
        if char in vowels or (char == "y" and not vowel_sound):
            is_vowel = True
            vowel_sound = True
            syllable += char
            if i + 1 == n:
                _syllables_.append(syllable)
            i += 1


        # if current character is a consonant
        else:
            consonant = word[i:i+2] if (word[i:i+2] in composite_consonants or word[i:i+2] == char*2) else char

            next = word[i + len(consonant)] if i + len(consonant) < n else ""

            next_consonant = (next not in vowels and next != "y" and next != char)


            added = False

            if next_consonant or not vowel_sound:
                syllable += consonant
                added = True


            if (next_consonant or vowel_sound):
                _syllables_.append(syllable)

                syllable = "" if added else consonant

                vowel_sound = False

            i += len(consonant)


    return _syllables_


def split_syllable(syllable):

    pre,vowel,post = "","",""

    i = 0

    n = len(syllable)

    while i<n and syllable[i] not in vowels:
        pre += syllable[i]
        i+=1
    while i<n and syllable[i] in vowels:
        vowel += syllable[i]
        i+=1

    post = syllable[i:]

    return pre,vowel,post

def syllable_distance(syllable1, syllable2):
    d = 0

    syllable1 = split_syllable(syllable1)
    syllable2 = split_syllable(syllable2)

    return d + distance_consonants(syllable1[0],syllable2[0]) + distance_all_vowels(syllable1[1],syllable2[1]) + distance_consonants(syllable1[2],syllable2[2])


def distance(word1,word2):

    d = 0

    i,j = 0,0
    syllables1 = syllables(word1)
    syllables2 = syllables(word2)

    n,m = len(syllables1), len(syllables2)

    while i<n or j<m:
        syllable1 = syllables1[i] if i<n else ""
        syllable2 = syllables2[j] if j < m else ""

        d += syllable_distance(syllable1,syllable2)
        i+=1
        j+=1
    return d


def closest_word(target_word, dictionary):
    return min(dictionary , key = lambda word:distance(word, target_word))


if __name__ == "__main__":
    from time import perf_counter

    start = perf_counter()

    print(syllables("plez"))
    print(syllables("please"))

    print(distance_consonants("z","s"))

    print(perf_counter() - start)
