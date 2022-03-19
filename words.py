import re

WORDS_LEN = 5
ALL_WORDS_PATH = "possible_words.txt"
ALL_WORDS_PATTERN = re.compile(f"\"([a-z]{{{WORDS_LEN}}})\"")
COMMON_WORDS_PATH = "common_words.txt"
COMMON_WORDS_PATTERN = re.compile(f"([A-Z]{{{WORDS_LEN}}})")

def findall_in_file(pattern, path):
    with open(path, 'rb') as f:
        return re.findall(pattern, f.read().decode())

def get_all_words():
    return list({word.lower() for word in findall_in_file(ALL_WORDS_PATTERN, ALL_WORDS_PATH)})

def get_common_words():
    return [word.lower() for word in findall_in_file(COMMON_WORDS_PATTERN, COMMON_WORDS_PATH)]
