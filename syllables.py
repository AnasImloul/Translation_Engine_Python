a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'

consonants = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}
composite_consonants = {"sh":{"ch"},"ch":{"sh"},"th":{d},"zz":{z,t+z},"ll":{l}, "ss":{s},"cu":q}

similar_sound = {"":{e}, a:{e,i},b:{p,v},c:{s,k},d:{},e:{a,y,""},f:{v},g:{j},h:{e,""},i:{e,a,y},j:{j},k:{c,q},l:{r},m:{n},n:{m},o:{u},p:{b},q:{c+u,k+u},r:{l},s:{c,z},t:{z},u:{y,o,a},v:{f,b},w:{v},x:{s,c,k},y:{i,e,u}, z:{s}}

vowels = {'a', 'e', 'i', 'o', 'u'}
composite_vowels = {"au":{o,u},"ae":{e}, "ea":{e,""},"oe":{e,""},"ie":{e,""},"eo":{"yo"}, "io":{"yo"},"oo":{o},"ee":{e,""}}




def clean(word):

    word = word.lower()

    result = ""

    n = len(word)

    i = 0

    while i < n:

        if i+1 < n and word[i + 1] == word[i]:
            result += word[i + 1] + word[i]

            i += 1

            while i + 1 < n and word[i + 1] == word[i]:
                i += 1

        else:
            result += word[i]

        i += 1

    return result


def next_syllable(word, i):
    syllable = word[i]

    n = len(word)

    if word[i] in consonants:

        i += 1

        while i < n and (syllable + word[i] in consonants or syllable + word[i] in composite_consonants):
            syllable += word[i]
            i += 1


        while i + len(syllable) <= n and (word[i:i + len(syllable)] == syllable):
            i += len(syllable)


        if i < n and word[i] in vowels:
            vowel = word[i]
            i += 1


            while i < n and (vowel + word[i] in vowels or vowel + word[i] in composite_vowels):
                vowel += word[i]
                i += 1

            while i + len(vowel) <= n and (word[i:i + len(vowel)] == vowel):
                i += len(vowel)

            syllable += vowel

    else:
        i += 1

        if i < n and word[i] in vowels:
            vowel = word[i]

            i += 1

            while i < n and (vowel + word[i] in vowels or vowel + word[i] in composite_vowels):
                vowel += word[i]
                i += 1

            while i + 1 <= n and (word[i] == vowel[-1]):
                i += len(syllable)
            syllable = vowel

    return syllable, i


def syllables(word):
    word = clean(word)

    n = len(word)

    s = []

    i = 0
    while i < n:
        syllable, i = next_syllable(word, i)

        s.append(syllable)

    return s


def dis(word1,word2):

    d = 0


    n,m = len(word1), len(word2)

    i,j = 0,0

    while i < n or j < m:

        char1 = ""
        char2 = ""



        while i < n and (char1 + word1[i] in vowels or char1 + word1[i] in consonants or char1 + word1[i] in composite_consonants or char1 + word1[i] in composite_vowels):
            char1 += word1[i]
            i+=1

        while j < m and (char2 + word2[j] in vowels or char2 + word2[j] in consonants or char2 + word2[j] in composite_consonants or char2 + word2[j] in composite_vowels):
            char2 += word2[j]
            j+=1


        if char1 != char2:
            similar = 0
            count = 0

            if char1 in similar_sound:
                similar += char2 not in similar_sound[char1]
                count += 1


            if char2 in similar_sound and f!=d:
                similar += char1 not in similar_sound[char2]
                count+=1


            if char1 in composite_vowels:
                similar += char2 not in composite_vowels[char1]
                count += 1

            if char2 in composite_vowels:
                similar += char1 not in composite_vowels[char2]
                count += 1


            if char1 in composite_consonants:
                similar += char2 not in composite_consonants[char1]
                count += 1


            if char2 in composite_consonants:
                similar += char1 not in composite_consonants[char2]
                count += 1

            if similar == count:
                d += 1

        else:
            d -= 1

    return d


def distance(word1,word2):
    d = 0

    word1 = clean(word1)
    word2 = clean(word2)

    syllables1 = syllables(word1)
    syllables2 = syllables(word2)

    n,m = len(syllables1), len(syllables2)


    if n>m:
        syllables1,syllables2 = syllables2, syllables1
        n,m = m,n



    for i in range(n):
        d+= dis(syllables1[i], syllables2[i])

    if m > n:
        d+= dis("", syllables2[n])


    return d

def closest_word(target_word, dictionary):

    return min(dictionary , key = lambda word:distance(word, target_word))


word1, word2 = "bbbbbbbbbbbbbbeeeeeeeeeeeeeeeeaaaaaaaaaaaaaaaaaaaaauuuuuuuuuuuuuuuuuuuuutttttttttttttttttiiiiiiiiiiiiiiiiiiiiifffffffffffffffffffuuuuuuuuuuuuuuuuuuuuulllllllllllllllll", "beautiful"
#print(syllables(word1), syllables(word2))

#print(distance(word1, word2))
