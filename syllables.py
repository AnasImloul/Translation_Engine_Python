a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z = 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'

consonants = {'b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z'}
composite_consonants = {"sh":{"ch"},"ch":{"sh"},"th":{d},"zz":{z,t+z},"ll":{l}, "ss":{s},"cu":q}

similar_sound = {"":{e}, a:{e,i},b:{p,v},c:{s,k},d:{},e:{a,y,""},f:{v},g:{j},h:{e,""},i:{e,a,y},j:{j},k:{c,q},l:{r},m:{n},n:{m},o:{u},p:{b},q:{c+u,k+u},r:{l},s:{c,z},t:{z},u:{y,o,a},v:{f,b},w:{v},x:{s,c,k},y:{i,e,u}, z:{s}}

vowels = {'a', 'e', 'i', 'o', 'u'}
composite_vowels = {"au":{o,u},"ae":{e}, "ea":{e,""},"oe":{e,""},"ie":{e,""},"eo":{"yo"}, "io":{"yo"},"oo":{o},"ee":{e,""}}


vowels = {"a","e","i","u","o"}



def clean_redundancy(word):
    result = ""
    current = word[0]
    count = 0

    i = 0

    n = len(word)

    while i < n:
        if current == word[i]:
            if count == 2 - (word[i] in vowels):
                i+=1
                continue
            result += word[i]
            count += 1
            i+=1

        else:
            current = word[i]
            count = 0
    return result



def syllables(word):


    n = len(word)

    vowel_sound = False
    current,count = word[0],0

    i = 0

    _syllables_ = []

    syllable = ""

    is_vowel = False

    while i < n:

        char = word[i]

        if current == char:
            if count == 2 - is_vowel:
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


        # if current character is a consonant
        else :
            is_vowel = False

            next_consonant = (i + 1 == n or (word[i+1] == "y" and word[i+1] != char))

            if next_consonant or not vowel_sound:
                syllable += char

            if vowel_sound:
                _syllables_.append(syllable)
                syllable = "" if next_consonant else char
                vowel_sound = False
        i += 1

    if syllable != "":
        if not vowel_sound:
            if syllable:
                _syllables_[-1] += syllable
            else:
                _syllables_.append(syllable)

        else:
            if syllable[-1] == "e":
                syllable = syllable[:-1]

            _syllables_.append(syllable)

    return _syllables_



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
