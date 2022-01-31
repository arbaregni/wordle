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
#       RIGHT_LETTER_AND_SPOT > RIGHT_LETTER > WRONG_LETTER > UNTESTED
RIGHT_LETTER_AND_SPOT = 2
RIGHT_LETTER = 1
WRONG_LETTER = 0
UNTESTED = -1 
    
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
    RIGHT_LETTER_AND_SPOT: '\033[32m',  # green
    RIGHT_LETTER: '\033[33m',           # yellow
    WRONG_LETTER: '\033[37m',           # white
    UNTESTED: '\033[30m',               # black
}
RED_BLUE_COLOR_SCHEME = {
    RIGHT_LETTER_AND_SPOT: '\033[31m',  # red
    RIGHT_LETTER: '\033[34m',           # blue
    WRONG_LETTER: '\033[37m',           # white
    UNTESTED: '\033[30m',               # black
}

CLEAR_LINE = '\033[A\033[2K\r'
RESET = '\033[0m'

def colorize(word, comparison, scheme):
    s = ''
    for ch, x in zip(word, comparison):
        s += '%s%c' % (scheme[x], ch)
    s += RESET
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

    print '%sRIGHT_LETTER_RIGHT_SPOT    %sRIGHT_LETTER%s' % (scheme[RIGHT_LETTER_AND_SPOT], scheme[RIGHT_LETTER], RESET)

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alpha_tracker = [UNTESTED for _ in alphabet]

    lineno = 0 # this is how many line numbers we have to jump to get back to the alphabet
    print 'Alpha: ' + colorize(alphabet, alpha_tracker, scheme=scheme); lineno += 1

    print; lineno += 1

    print 'Guesses: '; lineno += 1

    win = False
    for guessno in range(1, 7):
        prefix = '[%d] ' % guessno

        # -------- get the guess ------------
        guess = ''
        lineno += 1
        while True:
            guess = raw_input(prefix).strip().lower()
            if guess in wordset:
                break
            print CLEAR_LINE,

        # use the guess to provide more info to the user

        comparison = compare(right_word, guess)
        colorized_guess = colorize(guess, comparison, scheme=scheme)
        print CLEAR_LINE + '%s%s' % (prefix, colorized_guess)

        # ---------------------------
        #  keep track of the alphabet printed on the first line

        # update the alpha tracker to the information which conveys the most information
        for i,ch in enumerate(alphabet):
            j = guess.find(ch)
            if j == -1: continue

            if comparison[j] > alpha_tracker[i]:
                alpha_tracker[i] = comparison[j]

        if REPLACE_LINE:
            # move back to the top (NOTE: the lack of a newline here)
            print '\033[%dA\r' % lineno,
            # replace the line with the newly updated
            print 'Alpha: %s' % colorize(alphabet, alpha_tracker, scheme=scheme),
            # move back to current row
            print '\033[%dB\r' % lineno,

        # ----------------------------


        # Check for the winner

        if right_word == guess:
            win = True
            break


    if win:
        print 'Yay you got it!!!!'
    else:
        print 'The word was \033[31m%s\033[0m. Better luck next time.' % right_word

    return win

if __name__ == '__main__':
    main()
