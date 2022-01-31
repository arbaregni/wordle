from core import *
import sys

REPLACE_LINE = True

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

    oracle = Oracle.from_args(sys.argv)

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
            if oracle.is_valid(guess):
                break
            print CLEAR_LINE,

        # use the guess to provide more info to the user

        comparison = oracle.compare(guess)
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

        if oracle.is_right(guess):
            win = True
            break


    if win:
        print 'Yay you got it!!!!'
    else:
        print 'The word was \033[31m%s\033[0m. Better luck next time.' % oracle.right_word

    return win

if __name__ == '__main__':
    main()
