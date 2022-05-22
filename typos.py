def distance(word1,word2):

    i,j = 0,0

    n,m = len(word1), len(word2)

    distance = 0

    while i<n or j<m:

        previous1 = word1[i-1] if 0<=i-1<n else ""
        current1 = word1[i] if 0<=i<n else ""
        next1 = word1[i+1] if 0 <= i+1 < n else ""

        previous2 = word2[i - 1] if 0 <= i - 1 < m else ""
        current2 = word2[i] if 0 <= i < m else ""
        next2 = word2[i + 1] if 0 <= i + 1 < m else ""

        permutation_typo = sorted((previous1,current1,next1)) != sorted((previous2, current2, next2))

        misspell_typo = current1 != current2

        distance += permutation_typo + misspell_typo*(permutation_typo)
        i+=1
        j+=1

    return distance


def closest_word(target_word, dictionary):
    return min(dictionary, key = lambda word : distance(word, target_word))

if __name__ == "__main__":
    from time import perf_counter

    start = perf_counter()

    print(distance("aba","baa"))

    print(perf_counter() - start)