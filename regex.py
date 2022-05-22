



def regex_split(word):
    n = len(word)

    parts = []

    i = 0

    while i < n:
        if word[i] in "*.":
            parts.append(word[i])
            i += 1

        elif word[i] == "[":
            part = ""

            while i < n and word[i] != "]":
                if word[i] != " ":
                    part += word[i]
                i += 1

            if i < n:
                part += word[i]
                i += 1

            parts.append(part)
        else:
            part = ""
            while i < n and word[i] not in ".*[":
                part += word[i]
                i += 1
            parts.append(part)
    return parts


def regex(word, pattern):
    #TODO t*n == translation
    pattern = regex_split(pattern)

    reversed_word = word[::-1]

    n = len(word)

    i = 0

    for index, part in enumerate(pattern):

        if part == word[i:i + len(part)]:
            i += len(part)
            continue

        if part[0] not in ".*[":
            if part != word[i:i + len(part)]:
                return False

        if part == ".":
            i += 1
            continue

        if part[0] == "[" and part[-1] == "]":
            part = part[1:-1].split("-", 2)

            if len(part) == 1:
                if part == "":
                    continue

                if part != word[1:len(part)]:
                    return False

                else:
                    i += len(part)
                    continue

            else:
                if not (len(part[0]) == 1 and len(part[1]) == 1):
                    part[1], part[0] = part[0], part[1]

                is_between = False
                if part[0] == "":
                    if part[1] == "":
                        i += 1
                        continue

                    if word[i:i + 1] <= part[1]:
                        i += 1
                        continue

                    else:
                        return False

                if part[1] == "":
                    if word[i:i + 1] >= part[0]:
                        i += 1
                        continue
                    else:
                        return False

                else:
                    if part[0] <= word[i] <= part[1]:
                        i += 1
                        continue
                    else:
                        return False

        if part == "*":
            if index + 1 == len(pattern):
                i = max(len(word),i)

                break

            if pattern[index + 1] == part:
                index += 1
                continue

            try:
                i = n - 1 - reversed_word.index(pattern[index + 1][::-1],0,n-i)
            except:
                return False

    return i == len(word)


if __name__ == "__main__":
    print(regex("translation", "t*n"))
