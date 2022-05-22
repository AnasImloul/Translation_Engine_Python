import json
from json.decoder import JSONDecodeError
from os import getcwd, listdir, mkdir
from shutil import rmtree
from os.path import isdir, exists
import styleIO as style
from time import perf_counter,sleep
from sys import stdin, stdout
from threading import Lock
from regex import regex



lock = Lock()

commands = ["show", "add", "delete", "update"]

yes = {"y", "yes"}

path = ["languages"]

open_file = {"name": "", "file": None}


def print(s):
    lock.acquire()
    stdout.write(str(s))
    lock.release()

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


def remove_extension(file):
    n = len(file)

    reversed_file = file[::-1]

    if "." in reversed_file:
        return file[:n - 1 - reversed_file.index(".")]

    else:
        return file



def WrongArgumentError():
    print(style.RED + f"Error : Invalid arguments.\nfor more information type 'help'.\n" + style.RESET)

def WrongPathError():
    print(style.RED + "Error : You're not allowed to show words while working on this directory\n" + style.RESET)

def WrongCommandError():
    if path[-1] == "languages":
        WrongLanguageError()
        print("Available languages -> ")
        if not show_languages({"command": "*", "parameters": {}}, printable = False):
            print(style.RED + "None\n")
        else:
            show_languages({"command": "*", "parameters": {}}, printable=True)

    else:
        print(style.RED + "Error : Invalid command\n" + style.RESET)

def WrongLanguageError():
    print(style.RED + "Error : No such language found\n" + style.RESET)

def WrongWordError():
    print(style.RED + f"Error : {path[-2].capitalize()} dictionary does not contain such words\n" + style.RESET)

def LanguageAlreadyExistError(language):
    print(style.RED + f"Error : the language '{language.capitalize()}' already exist\n")

def LanguageNotExistError(language):
    print(style.RED + f"Error : the language '{language.capitalize()}' does not exist\n")

def WordAlreadyExistError(word, language):
    print(style.RED + f"Error : '{word}' already exists in the {language.capitalize()} dictionary\n" + style.RESET)

def WordNotExistError(word, language):
    print(style.RED + f"Error : '{word}' does not exist in the {language.capitalize()} dictionary\n")


def HomonymAlreadyExistError(homonym):
    print(f"Error : can't add '{homonym}', it already exists\n")

def WrongInputFormatError():
    print(style.RED + "Error : Invalid input\n" + style.RESET)



def clean(command):
    command = command.split()

    clean = {"command": [], "parameters": dict()}

    index = 0

    n = len(command)

    while index < n and not command[index].startswith("-"):
        clean["command"].append(command[index])
        index += 1

    parameters = " ".join(command[index:]).split(" -")

    for parameter in parameters:
        parameter = parameter.split(" ", 1)

        if parameter[0] != "":
            if len(parameter) != 2:
                argument, value = parameter[0], ""
            else:
                argument, value = parameter
            if "-" in argument:
                argument = argument[argument.index("-") + 1:]

            clean["parameters"][argument] = value

    return clean


def save(open_file):
    if exists(open_file["name"]):
        with open(open_file["name"], 'w') as out_file:
            out_file.write(json.dumps(open_file["file"], indent=4))


def cd(command):
    global open_file

    if command["command"][0] == ".." and len(path) > 1:
        path.pop()
        command["command"].pop(0)

        save(open_file)

        open_file = {"name": "", "file": None}
        return

    try:
        all_dir_files = map(lambda word: (word if "." not in word else word[:word.index(".")]),
                            listdir(getcwd() + "/" + "/".join(path)))

    except:
        return

    if command["command"][0] in all_dir_files:
        path.append(command["command"][0])
        command["command"].pop(0)
        return True


    else:
        return False


def cd_all(command):
    n = len(command["command"])

    i = 0
    while i < n and cd(command):
        i += 1


def help_languages(command):
    print("sorry, I can't help you. I couldn't even help myself :(\n")


def add_languages(command):
    if len(command["command"]) < 1:
        WrongArgumentError()
        return False

    languages_path = f"{getcwd()}/{'/'.join(path)}"

    language = command["command"][0]

    language_path = languages_path + f"/{language}"

    if isdir(language_path):
        LanguageAlreadyExistError(language)
        return False

    else:
        confirm = input(
            f"Add {style.LIGHT_GREEN + language.capitalize() + style.RESET} ?\nType 'y' or 'yes' to confirm : ")
        if confirm.lower() in yes:
            mkdir(language_path)
            open(language_path + "/words.json", "w").close()
            print(f"{style.LIGHT_GREEN + language.capitalize() + style.RESET} added successfully !\n")

        else:
            print(f"Addition canceled\n")

        print("_" * 26 + "\n")

    return confirm.lower() in yes


def delete_languages(command):
    if len(command["command"]) < 1:
        WrongArgumentError()
        return False

    languages_path = f"{getcwd()}/{'/'.join(path)}"

    regex_language = command["command"][0]

    all_languages = listdir(languages_path)

    languages = list(filter(lambda language: regex(language, regex_language), all_languages))

    for language in languages:
        language_path = languages_path + f"/{language}"

        if not isdir(language_path):
            print(
                f"{style.RED + 'Error' + style.RESET} : '{style.LIGHT_GREEN + language.capitalize() + style.RESET}' language does not exist\n")
        else:
            confirm = input(
                f"Delete {style.LIGHT_GREEN + language.capitalize() + style.RESET} ?\nType 'y' or 'yes' to confirm : ")
            if confirm.lower() in yes:
                rmtree(language_path)
                print(f"{style.LIGHT_GREEN + language.capitalize() + style.RESET} deleted successfully !\n")

            else:
                print(f"deletion canceled\n")

            print("_" * 26 + "\n")

    if len(languages) == 0:
        WrongLanguageError()
        return False

    return True


def show_languages(command,printable = True):
    languages_path = f"{getcwd()}/{'/'.join(path)}"
    all_languages = listdir(languages_path)


    if len(command["command"]) > 1:
        if printable:
            WrongArgumentError()
        return False

    search = "*"

    if len(command["command"]) == 1:
        search = command["command"][0]

    all_languages = list(filter(lambda language: regex(language, search), all_languages))

    if len(all_languages) == 0:
        if printable:
            WrongLanguageError()
        return False

    if printable:
        print(style.LIGHT_GREEN + " ".join(all_languages) + style.RESET + "\n")

    return True


def show_inLanguage(command, printable = True):

    language_path = f"{getcwd()}/{'/'.join(path)}"
    all_files = listdir(language_path)

    if len(command["command"]) > 0:
        if printable:
            WrongArgumentError()
        return False


    if len(all_files) == 0:
        if printable:
            WrongLanguageError()
        return False

    if printable:
        print(style.LIGHT_GREEN + " ".join(map(lambda file : remove_extension(file),all_files)) + style.RESET + "\n")

    return True


def delete_words(command):
    words_path = getcwd() + "/" + "/".join(path) + ".json"

    if len(path) < 2:
        WrongPathError()
        return False

    if len(command["command"]) != 1:
        WrongArgumentError()
        return False

    if open_file["name"] != words_path:
        with open(words_path, 'r') as in_file:
            try:
                data = json.loads(in_file.read())
            except JSONDecodeError:
                data = dict()

        open_file["name"] = words_path
        open_file["file"] = data

    regex_word = ""

    if len(command["command"]) != 0:
        regex_word = command['command'][0]

    words = list(filter(lambda word: regex(word, regex_word), sorted(open_file["file"].keys())))

    for word in words:
        open_file["file"].pop(word)

    if len(words) == 0:
        WrongWordError()
        return False

    return True


help = {
    "add" : "",
    "delete" : "",
    "show" : "",
    "update" : ""
}


# TODO complete help command
def help_words(command):
    print(f"""┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│_____________________________________{style.GREEN}Welcome to Words help utility!{style.RESET}__________________________________________│
│                                                                                                             │
│                                                                                                             │
│Enter the name of any supported command to either add, update, show or delete words from the dictionnary.    │
│{style.CYAN}__supported commands__{style.RESET}                                                                                       │
│    {style.LIGHT_GREEN}__add__{style.RESET}                                                                                                  │
│        \\\\__command_line example__//{style.RESET}                                                                         │
│            {style.BLUE}/languages/english/words${style.RESET} add beautiful -t adjective -s attractive,pretty,pleasing -a ugly       │
│                                                                                                             │
│        \\\\__arguments__//{style.RESET}                                                                                    │
│            the command {style.LIGHT_GREEN}'add'{style.RESET} has only one argument                                                          │
│                                                                                                             │
│                __wordname__{style.RESET}                                                                                 │
│                    the name of the word needed to be added into the dictionary                              │
│                                                                                                             │
│        \\\\__parameters__//{style.RESET}                                                                                   │
│            the command {style.LIGHT_GREEN}'add'{style.RESET} has 5 different parameters (they are all optional)                             │
│                                                                                                             │
│            -d    set a definition to the word                                                               │
│            -t    set the type of the word (verb, noun, adjective, adverb, ...)                              │
│            -e    give an example of the word in a sentence                                                  │
│            -s    give a list of synonyms of the word (synonyms are separated by a colon ',')                │
│            -a    give a list of antonyms of the word (antonyms are separated by a colon ',')                │
│                                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
""")


def add_words(command):
    words_path = getcwd() + "/" + "/".join(path) + ".json"

    if len(path) < 2:
        WrongPathError()
        return False

    if len(command["command"]) != 1:
        WrongArgumentError()
        return False

    if open_file["name"] != words_path:
        with open(words_path, 'r') as in_file:
            try:
                data = json.loads(in_file.read())

            except JSONDecodeError:
                data = dict()

        open_file["name"] = words_path
        open_file["file"] = data

    word = command["command"][0]

    if word in open_file["file"]:
        WordAlreadyExistError(word, path[-2])
        return False

    open_file["file"][word.lower()] = command["parameters"]
    print(f"'{style.LIGHT_GREEN + word + style.RESET}' added to the dictionary!\n")

    return True


def feed_words(command):
    words_path = getcwd() + "/" + "/".join(path) + ".json"

    if len(path) < 2:
        WrongPathError()
        return False

    if len(command["command"]) < 1:
        WrongArgumentError()
        return False

    if open_file["name"] != words_path:
        with open(words_path, 'r') as in_file:
            try:
                data = json.loads(in_file.read())

            except JSONDecodeError:
                data = dict()

        open_file["name"] = words_path
        open_file["file"] = data

    text = " ".join(command["command"])
    text = ("".join(list(filter(lambda x : x.isalpha() or x == ' ', text.lower())))).split()

    new_words = 0

    for word in text:
        if word not in open_file["file"]:
            open_file["file"][word] = dict()
            new_words += 1

    print(f"This text added {style.LIGHT_GREEN + str(new_words) + style.RESET} new words to the dictionary!\n")
    return True

def show_words(command, printable = True):
    words_path = getcwd() + "/" + "/".join(path) + ".json"

    if len(path) < 2:
        WrongPathError()
        return False


    if len(command['command']) > 1:
        WrongArgumentError()
        return False

    if open_file["name"] != words_path:
        with open(words_path, 'r') as in_file:
            try:
                data = json.loads(in_file.read())
            except JSONDecodeError:
                data = dict()

        open_file["name"] = words_path
        open_file["file"] = data


    if len(command["command"]) == 0:
        print(style.LIGHT_GREEN + str(len(open_file["file"])) + " word\n")
        return True

    if len(open_file["file"]) == 0:
        print("Dictionary is empty\n")
        return False

    if len(command["parameters"]) == 0:
        parameters = ""

    else:
        parameters = "".join(command["parameters"])
        parameters.replace("-", "")

    regex_word = command['command'][0]

    words = list(filter(lambda word: regex(word, regex_word), sorted(open_file["file"].keys())))

    for word in words:

        print(style.LIGHT_GREEN + word + style.RESET + "\n")

        word = open_file["file"][word]

        if 'd' in parameters and 'd' in word:
            print(f"Definition : {word['d']}\n")

        if 't' in parameters and 't' in word:
            print(f"Type : {word['t']}\n")

        if 'e' in parameters and 'e' in word:
            print(f"Example : {word['e']}\n")

        if 's' in parameters and 's' in word:
            print(f"Synonyms : {word['s']}\n")

        if 'a' in parameters and 'a' in word:
            print(f"Antonyms : {word['a']}\n")

        print("_"*26+"\n")

    if len(words) == 0:
        print("Couldn't find what you're searching for\n")
        return False

    return True


def save_words(command):
    save(open_file)


def update_words(command):
    words_path = getcwd() + "/" + "/".join(path) + ".json"

    if len(path) < 2:
        WrongPathError()
        return False

    if open_file["name"] != words_path:
        with open(words_path, 'r') as in_file:
            try:
                data = json.loads(in_file.read())
            except JSONDecodeError:
                data = dict()

        open_file["name"] = words_path
        open_file["file"] = data

    word = command["command"][0]

    if word not in open_file["file"]:
        WordNotExistError(word, path[-2])
        return False

    open_file["file"][command["command"][0].lower()] = {**open_file["file"][command["command"][0]], **command["parameters"]}
    return True


functions = {"add_languages": add_languages, "delete_languages": delete_languages, "show_languages": show_languages, "help_languages" : help_languages,
             "show_inLanguage" : show_inLanguage,
             "add_words": add_words, "delete_words": delete_words, "update_words": update_words,"feed_words" : feed_words,
             "help_words": help_words,
             "show_words": show_words, "save_words": save_words
             }

print(style.BLUE + "/" + "/".join(path) + "$ " + style.RESET)
command = input()

start = perf_counter()

while command != "quit":
    if command.replace(" ", "") == "quit":
        break

    command = clean(command)

    cd_all(command)

    if len(command["command"]) != 0:
        try:
            _command_ = command["command"].pop(0)
            if len(path) > 1 and path[-2] == "languages":
                functions[f"{_command_}_inLanguage"](command)
            else:
                functions[f"{_command_}_{path[-1]}"](command)

        except:
            save(open_file)
            WrongCommandError()

    print(style.BLUE + "/" + "/".join(path) + "$ " + style.RESET)
    command = input()

print(str(perf_counter() - start) + "\n")

save(open_file)
