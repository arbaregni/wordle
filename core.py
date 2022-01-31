import random
import sys
from collections import Counter

WORD_FILE = r'./words.txt'
COMMON_WORD_FILE = r'./google-10000-english-usa.txt'

WORDSET = set()

with open(WORD_FILE) as infile:
    for line in infile:
        w = line.strip().lower()
        if len(w) != 5: continue
        WORDSET.add(w)

COMMON_WORDS = []

with open(COMMON_WORD_FILE) as infile:
    for line in infile:
        w = line.strip().lower()
        if len(w) != 5: continue
        WORDSET.add(w)
        COMMON_WORDS.append(w)

# constants used for comparing the output of a guess
# we must guarantee that
#       RIGHT_LETTER_AND_SPOT > RIGHT_LETTER > WRONG_LETTER > UNTESTED
RIGHT_LETTER_AND_SPOT = 2
RIGHT_LETTER = 1
WRONG_LETTER = 0
UNTESTED = -1 

class Oracle():
    def __init__(self, right_word, domain):
        self.right_word = right_word 
        self.domain = domain
    @staticmethod
    def from_args(args):
        choose_from = COMMON_WORDS
        if '--hard' in args:
            choose_from = tuple(WORDSET)

        right_word = random.choice(choose_from)

        for arg in args:
            if arg.startswith('--pick='):
                right_word = arg[len('--pick='):]

        return Oracle(right_word, WORDSET)

    def is_valid(self, guess):
        return guess in self.domain
    def is_right(self, guess):
        return self.right_word == guess
    def compare(self, guess):
        answer = [WRONG_LETTER for _ in guess]
        counter = Counter(self.right_word)
        n = len(guess)

        for i in range(n):
            if i < len(self.right_word) and self.right_word[i] == guess[i]:
                counter[guess[i]] -= 1
                answer[i] = RIGHT_LETTER_AND_SPOT
        
        for i in range(n):
            if answer[i] == RIGHT_LETTER_AND_SPOT:
                continue

            ch = guess[i]
            if counter[ch] > 0:
                counter[ch] -= 1
                answer[i] = RIGHT_LETTER

        return answer
