composite_consonants = {
    "sh": {"ch": 1},
    "ch": {"sh": 1},
    "gh": {"g": 2},
    "sc": {"s": 1, "sk": 2},
    "ph": {"f": 1},
    "ck": {"k": 1, "q": 1},
    "ng": {"n": 1, "g": 1},
    "sk": {"sc": 2},
}

consonants = {
    'b': {"p": 3, "v": 3},
    'q': {"c": 2, "k": 3},
    's': {"c": 3, "z": 2},
    'z': {"s": 2}
}

for char in "bcdfghjklmnpqrstvwxyz":
    if char not in consonants:
        consonants[char] = dict()

_consonants_ = consonants.keys() | composite_consonants.keys()

y = {"i":1,"u":2,"e":3}

vowels = {
    "a": {"e": 1, "i": 1, "": 2},
    "e": {"a": 1, "i": 3, "": 0},
    "i": {"e": 1, "a": 1, "": 3},
    "o": {"u": 2, "": 4},
    "u": {"o": 2, "a": 3, "": 5},
    "": {"e": 1}
}

composite_vowels = {
    "au": {"o": 1, "u": 2, "": 5},
    "ou": {"o": 1, "u": 2, "": 4},
    "ea": {"e": 1, "": 1, "a": 2, "i": 3},
    "ae": {"e": 1, "a": 2, "i": 3, "": 3},
    "oe": {"e": 1, "o": 2, "": 3},
    "ee":{"e":1},
    "oo":{"o":1},
    "ii":{"i":1},
    "aa":{"a":1},
    "oo":{"o":1}
}

all_vowels = {**vowels, **composite_vowels}


def current_vowel(word, i):
    if i < len(word):
        if i + 1 < len(word) and word[i:i + 2] in composite_vowels:
            return word[i:i + 2], i + 2
        else:
            return word[i], i + 1
    return "", i+1


def distance_vowels(vowel1, vowel2):
    if vowel1 == vowel2:
        return 0


    d = 8

    if vowel1 == "y":
        if vowel2 in composite_vowels:
            intersect = composite_vowels[vowel2].keys() + vowel1.key()
            for vowel in intersect:
                d = min(d, y[vowel], composite_vowels[vowel2][vowel])
        else:
            d = y.get(vowel2,d)
        return d

    if vowel2 == "y":
        if vowel1 in composite_vowels:
            intersect = composite_vowels[vowel1].keys() + vowel2.key()
            for vowel in intersect:
                d = min(d, y[vowel], composite_vowels[vowel1][vowel])
        else:
            d = y.get(vowel1,d)
        return d






    parents1 = {}
    parents2 = {}


    if vowel1 in composite_vowels:
        parents1 = composite_vowels[vowel1]

        if vowel2 in composite_vowels:
            parents2 = composite_vowels[vowel2]

            intersect = parents1.keys() & parents2.keys()

            for vowel in intersect:
                d = min(d, parents1[vowel], parents2[vowel])

            return d

        elif vowel2 in vowels:
            d = parents1.get(vowel2, d)
            return d

    elif vowel1 in vowels:

        if vowel2 in composite_vowels:
            parents2 = composite_vowels[vowel2]

            if vowel1 in vowels:
                d = parents2.get(vowel1, d)

                return d
        elif vowel2 in vowels:
            d = min(vowels[vowel2].get(vowel1, d), vowels[vowel1].get(vowel2, d))
            return d

    return d


def distance_all_vowels(vowel1, vowel2):
    i, j = 0, 0

    n, m = len(vowel1), len(vowel2)

    d = 0


    while i < n or j < m:
        current1, i = current_vowel(vowel1, i)
        current2, j = current_vowel(vowel2, j)

        d += distance_vowels(current1, current2)

    return d


def distance_consonants(consonant1, consonant2):
    if consonant1 == consonant2:
        return 0



    if len(consonant1) == 2:
        if len(consonant2) == 1:
            if consonant1 == 2*consonant2:
                return 1

    if len(consonant2) == 2:
        if len(consonant1) == 1:
            if consonant2 == 2*consonant1:
                return 1



    parents1 = {}
    parents2 = {}

    d = 8

    if consonant1 in composite_consonants:
        parents1 = composite_consonants[consonant1]

        d = parents1.get(consonant2, d)

        if consonant2 in composite_consonants:
            parents2 = composite_consonants[consonant2]

            d = parents2.get(consonant1, d)

            return d

        elif consonant2 in consonants:
            d = parents1.get(consonant2, d)
            return d

    elif consonant1 in consonants:

        if consonant2 in composite_consonants:
            parents2 = composite_consonants[consonant2]

            if consonant1 in consonants:
                d = parents2.get(consonant1, d)
                return d
        elif consonant2 in consonants:
            # use only one way distance since we want to check similarity to the dictionary and not the reversed direction
            d = min((consonants[consonant1].get(consonant2, d), consonants[consonant2].get(consonant1, d)))
            return d

    return d


def syllables(word):
    _syllables_ = []
    is_vowel = False

    n = len(word)

    i = 0

    syllable = ""

    while i < n:
        if word[i] in vowels:
            syllable += word[i]
            is_vowel = True
            while i + 1 < n and word[i + 1] in vowels:
                syllable += word[i + 1]
                i += 1

            _syllables_.append(syllable)
            syllable = ""

        else:
            if not is_vowel:
                if word[i] == "y":
                    _syllables_.append("y")
                    i+=1
                    continue
                else:
                    _syllables_.append("")

            is_vowel = False

            syllable += word[i]

            while i + 1 < n and (syllable + word[i + 1] in _consonants_ or syllable == word[i+1]):
                syllable += word[i + 1]
                i += 1
            _syllables_.append(syllable)
            syllable = ""
        i += 1

    return _syllables_


def distance(word1, word2):
    d = 0
    i, j = 0, 0
    syllables1 = syllables(word1)
    syllables2 = syllables(word2)

    n, m = len(syllables1), len(syllables2)

    while i < max(n, m):
        syllable1 = syllables1[i] if i < n else ""
        syllable2 = syllables2[i] if i < m else ""

        if i % 2 == 0:


            d += distance_all_vowels(syllable1, syllable2)

        else:
            d += distance_consonants(syllable1, syllable2)

        i += 1

    return d


def closest_word(target_word, dictionary):
    return min(dictionary, key=lambda word: distance(word, target_word))


if __name__ == "__main__":
    from time import perf_counter

    start = perf_counter()

    print(perf_counter() - start)
