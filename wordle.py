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


CORRECT_LETTER_CORRECT_POSITION = 0
CORRECT_LETTER_WRONG_POSITION = 1
WRONG_LETTER = 2
def compare(fixed_word, word):
    answer = [WRONG_LETTER for _ in fixed_word]
    counter = Counter(fixed_word)

    for i in range(len(fixed_word)):
        if fixed_word[i] == word[i]:
            counter[word[i]] -= 1
            answer[i] = CORRECT_LETTER_CORRECT_POSITION
    
    for i in range(len(fixed_word)):
        if answer[i] == CORRECT_LETTER_CORRECT_POSITION:
            continue

        ch = word[i]
        if counter[ch] > 0:
            counter[ch] -= 1
            answer[i] = CORRECT_LETTER_WRONG_POSITION

    return answer

GREEN_YELLOW_COLOR_SCHEME = {
    CORRECT_LETTER_CORRECT_POSITION: '\033[32m',
    CORRECT_LETTER_WRONG_POSITION: '\033[33m',
    WRONG_LETTER: '\033[37m'
}
RED_BLUE_COLOR_SCHEME = {
    CORRECT_LETTER_CORRECT_POSITION: '\033[31m',
    CORRECT_LETTER_WRONG_POSITION: '\033[34m',
    WRONG_LETTER: '\033[37m'
}

CLEAR_LINE = '\033[A\033[2K\r'

def colorize(word, answer, prefix, scheme=GREEN_YELLOW_COLOR_SCHEME):
    s = prefix
    for ch, x in zip(word, answer):
        s += '%s%c' % (scheme[x], ch)
    s += '\033[0m' # text reset
    print s

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

    fixed_word = random.choice(choose_from)

    for arg in sys.argv:
        if arg.startswith('--pick='):
            fixed_word = arg[len('--pick='):]

    scheme = GREEN_YELLOW_COLOR_SCHEME
    if '--riaz' in sys.argv:
        scheme = RED_BLUE_COLOR_SCHEME

    print

    win = False
    for i in range(6):
        prefix = '[%d] ' % (i+1)
        if REPLACE_LINE:
            prefix = CLEAR_LINE + prefix


        while True:
            word = raw_input(prefix).strip().lower()
            if word in wordset:
                break
            ## time.sleep(0.5)


        answers = compare(fixed_word, word)
        colorize(word, answers, prefix, scheme=scheme)

        if fixed_word == word:
            print 'Yay you got it!!!!'
            win = True
            break

        print

    if not win:
        print 'The word was \033[31m%s\033[0m. Better luck next time.' % fixed_word

    return win

if __name__ == '__main__':
    main()
