import time
import random
import sys
from collections import Counter

WORD_LIST = r'./words.txt'
COMMON_WORD_LIST = r'./google-10000-english-usa.txt'

REPLACE_LINE = True

wordset = set()

with open(WORD_LIST) as infile:
    for line in infile:
        w = line.strip().lower()
        if len(w) != 5: continue
        wordset.add(w)

common_words = []

with open(COMMON_WORD_LIST) as infile:
    for line in infile:
        w = line.strip().lower()
        if len(w) != 5: continue
        wordset.add(w)
        common_words.append(w)

# constants used for comparing the output of a guess
# we must guarantee that
#       RIGHT_LETTER_AND_SPOT > RIGHT_LETTER > WRONG_LETTER
RIGHT_LETTER_AND_SPOT = 2
RIGHT_LETTER = 1
WRONG_LETTER = 0


## class Constraint():
## 
##     @staticmethod
##     def from(right_word, guess):
##         new = Constraint()
## 
##         comparison = compare(right_word, guess)
## 
##         # check for right letter, right spot
##         for i in range(len(right_word)):
##             if comparison[i] == RIGHT_LETTER_AND_SPOT:
##                 # the right word must include that letter at that spot
##                 new.includes.append( (right_word[i], i) )
##             elif comparison[i] == RIGHT_LETTER:
##                 # the right word must include that letter (at any position)
##                 new.includes.append( (right_word[i], None) )
##                 # but it can't include that letter at that spot
##                 new.excludes.append( (right_word[i], i) )
##             else:
##                 # the right letter may not include that letter
##                 new.excludes.append( (right_word[i], None) )
##     @staticmethod
##     def _predicate(predicate, word):
##         letr, spot = predicate
##         if spot is None:
##             return letr in word
##         else:
##             return letr == word[spot]
## 
##     def __init__(self):
##         """the empty constraint"""
##         self.includes = []
##         self.excludes = []
## 
##     def accepts(self, word):
##         for pred in self.includes:
##             if not Constraint._predicate(pred, word): return False
## 
##         for pred in self.excludes:
##             if Constraint._predicate(pred, word): return False
## 
##         return True

    
    
def compare(right_word, guess):
    answer = [WRONG_LETTER for _ in right_word]
    counter = Counter(right_word)

    for i in range(len(right_word)):
        if right_word[i] == guess[i]:
            counter[guess[i]] -= 1
            answer[i] = RIGHT_LETTER_AND_SPOT
    
    for i in range(len(right_word)):
        if answer[i] == RIGHT_LETTER_AND_SPOT:
            continue

        ch = guess[i]
        if counter[ch] > 0:
            counter[ch] -= 1
            answer[i] = RIGHT_LETTER

    return answer

GREEN_YELLOW_COLOR_SCHEME = {
    RIGHT_LETTER_AND_SPOT: '\033[32m',
    RIGHT_LETTER: '\033[33m',
    WRONG_LETTER: '\033[37m'
}
RED_BLUE_COLOR_SCHEME = {
    RIGHT_LETTER_AND_SPOT: '\033[31m',
    RIGHT_LETTER: '\033[34m',
    WRONG_LETTER: '\033[37m'
}

CLEAR_LINE = '\033[A\033[2K\r'

def colorize(word, comparison, scheme):
    s = ''
    for ch, x in zip(word, comparison):
        s += '%s%c' % (scheme[x], ch)
    s += '\033[0m' # text reset
    return s

def main():
    if '--help' in sys.argv:
        print 'wordle.py:'
        print '   --hard       use the expanded list of words'
        print '          (i.e, not the 10 000 most common)'
        print '   --help       display this message'
        print '   --pick=word  use word as the chosen word' 
        print '   --riaz       use the alternate color scheme'


    choose_from = common_words
    if '--hard' in sys.argv:
        choose_from = tuple(wordset)

    right_word = random.choice(choose_from)

    for arg in sys.argv:
        if arg.startswith('--pick='):
            right_word = arg[len('--pick='):]

    scheme = GREEN_YELLOW_COLOR_SCHEME
    if '--riaz' in sys.argv:
        scheme = RED_BLUE_COLOR_SCHEME

    print

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alpha_tracker = [WRONG_LETTER for _ in alphabet]

    print colorize(alphabet, alpha_tracker, scheme)
    print
    print

    win = False
    for i in range(6):
        prefix = '[%d] ' % (i+3)
        if REPLACE_LINE:
            prefix = CLEAR_LINE + prefix


        guess = ''
        while True:
            guess = raw_input(prefix).strip().lower()
            if guess in wordset:
                break
            ## time.sleep(0.5)

        # use the guess to provide more info to the user

        comparison = compare(right_word, guess)
        colorized_guess = colorize(guess, comparison, scheme=scheme)
        print '%s%s' % (prefix, colorized_guess)


        # ---------------------------
        #  keep track of the alphabet printed on the first line

        if REPLACE_LINE:
            # move back to the top
            print '\033[%dA' % (i+4)

        # update the alpha tracker to the information which conveys the most information
        for i,ch in enumerate(alphabet):
            j = guess.find(ch)
            if j == -1: continue

            if comparison[j] > alpha_tracker[i]:
                alpha_tracker[i] = comparison[j]

        # this moves us down 1
        print colorize(alphabet, alpha_tracker, scheme=scheme)

        if REPLACE_LINE:
            # move back to current row
            print '\033[%dB' % (i+3)

        # ----------------------------


        # Check for the winner

        if right_word == guess:
            print 'Yay you got it!!!!'
            win = True
            break

        print

    if not win:
        print 'The word was \033[31m%s\033[0m. Better luck next time.' % right_word

    return win

if __name__ == '__main__':
    main()
