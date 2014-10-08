# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
# http://www.codeskulptor.org/#user38_zktu02vHlwnFGCC.py

import random
import simpleguitk as simplegui

# helper function to start and restart the game
def new_game():
    """
    new_game() - starts a new game based on current range
    """

    # initialize global variables used in your code here
    global range
    global secret_number
    global guesses_left

    # set the secret number
    secret_number = random.randrange(0,range)

    #blank line before new game, looks better
    print

    # 7 guesses for [0,100), 10 for [0,1000)
    if range == 100:
        guesses_left = 7
    else:
        guesses_left = 10

    print "New Game"
    print "I'm thinking of a number between 0 and",range,"..."
    print "You have",guesses_left,"guesses left"

    # un-comment below for an easy game (or debugging)
    #print '(hint: secret number is',secret_number,')'

# define event handlers for control panel
def range100():
    """
    range100() - set the range to [0,100)
    """
    # button that changes the range to [0,100) and starts a new game
    global range
    global range_label

    # change label text
    range_label.set_text('Current game, range: 0-100')
    # set range
    range = 100
    # start new game
    new_game()

def range1000():
    """
    range1000() - set the range to [0,1000)
    """
    # button that changes the range to [0,1000) and starts a new game
    global range
    global range_label

    # change label text
    range_label.set_text('Current game, range: 0-1000')
    # set range
    range = 1000
    # start new game
    new_game()

def input_guess(guess):
    """
    input_guess() - handler for guess text input, this contains most of the
                    logic for the game
    """

    # main game logic goes here
    global inp
    global guesses_left

    # set input text to blank, ready for next guess
    inp.set_text('')

    # if guess is not a number let the user know
    # if we wanted to be mean we could reduce the number of guesses here
    if not guess.isdigit():
        print "please guess a NUMBER"
        return

    # convert input to number
    guess_num = int(guess)

    # output the guess
    print "Guess was",guess_num

    # if they got it right, tell them and start a new game
    if guess_num == secret_number:
        print "Correct - you won!"
        new_game()
        return

    # otherwise reduce the number of guesses left and check whether they've
    # run out. If so start a new game.
    guesses_left = guesses_left - 1
    if guesses_left == 0:
        print "You've run out of guesses! The secret number was", secret_number
        new_game()
        return

    #otherwise let the user know how they did
    if guess_num < secret_number:
        print "Higher"
    else:
        print "Lower"

    #and tell them how many more guesses they have
    print "You have",guesses_left,"guesses left"


# create frame
frame =  simplegui.create_frame('Guess the Number', 200, 200)

frame.add_button('Range: 0-100',range100)
frame.add_button('Range: 0-1000',range1000)
range_label = frame.add_label('Current game, range: 0-100')
range = 100

# register event handlers for control elements and start frame
inp = frame.add_input('Guess:',input_guess,50)


# call new_game
new_game()
frame.start()

# always remember to check your completed program against the grading rubric
