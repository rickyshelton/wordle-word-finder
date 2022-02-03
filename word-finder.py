
#!/usr/bin/python

import sys, getopt

# defaults
WORDS_FILE = "/usr/share/dict/words"
RANKED_LETTERS = "etaoinshrdlcumwfgypbvkjxqz"

# a list of letters known to be in the word
MUST_CONTAIN = []

# a list of letters known to not be in the word
MUST_NOT_CONTAIN = []

# known letters in their position
# ie - 'CHA--'
KNOWN_LETTERS = '-----'

# a list of tuples, each tuple is a letter and it's position
# ie - [('e', 0), ('t', 1)]]
KNOWN_INCORRECT_POSITIONS=[]

WORD_SCORE_TUPLES = []

def word_contains_all_letters(word: str, letters:list) -> bool:
    for letter in letters:
        if letter not in word:
            return False
    return True

def word_includes_any_letters(word: str, letters: list) -> bool:
    for letter in letters:
        if letter in word:
            return True
    return False

def all_unique_letters(word: str) -> bool:
    for letter in word:
        if word.count(letter) > 1:
            return False
    return True

def calculate_score(word: str) -> int:
    score = 0
    for letter in word:
        score += RANKED_LETTERS.index(letter)
    return score

def matches_known_letters(word: str, KNOWN_LETTERS: str) -> bool:
    for i in range(len(word)):
        if KNOWN_LETTERS[i] != '-' and word[i] != KNOWN_LETTERS[i]:
            return False
    return True

def matches_known_incorrect_positions(word: str, KNOWN_INCORRECT_POSITIONS: list) -> bool:
    for letter_pos in KNOWN_INCORRECT_POSITIONS:
        if word[letter_pos[1]] == letter_pos[0]:
            return True
    return False

def keep_word(word: str) -> bool:

    if not all_unique_letters(word):
        return False
    
    if not matches_known_letters(word, KNOWN_LETTERS):
        return False
    
    if word_includes_any_letters(word, MUST_NOT_CONTAIN):
        return False

    if not word_contains_all_letters(word, MUST_CONTAIN):
        return False

    if matches_known_incorrect_positions(word, KNOWN_INCORRECT_POSITIONS):
        return False

    return True

def main():

    # load words file
    with open(WORDS_FILE, 'r') as file:
        words = file.read().splitlines()

    # drop words that are not 5 letters long, convert to lower case
    words = [word.lower() for word in words if len(word) == 5]

    # dedupe the list and sort it
    words = sorted(set(words))

    # drop words that don't fit existing criteria
    words = [word for word in words if keep_word(word)]

    for word in words:
        WORD_SCORE_TUPLES.append((word, calculate_score(word)))

    sorted_word_tuples = sorted(WORD_SCORE_TUPLES, key=lambda x: x[1])
    print(sorted_word_tuples[:10])

if __name__ == "__main__":
    main()
