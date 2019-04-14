# implementation of card game - Memory
# Codeskulptor URL:

try:
    import simplegui
except:
    import simpleguitk as simplegui

import random

# card size
CARD_WIDTH = 88
CARD_HEIGHT = 120

# game play variables
game_state = 0
card1 = card2 = -1
turns = 0
pairs = 0
WINNING_PAIRS = 8

# loaded and picture_version are for when images are loading
loaded = 0
picture_version = False
NUM_IMAGES = 1
STATE_PRELOAD = 0
STATE_PLAYING = 1
STATE_WON = 2
program_state = STATE_PRELOAD

# image load statuses
NOTHING_LOADED=0
BACK_LOADED=1
IM_LOADED=2
load_status=NOTHING_LOADED

# Explanation of the process of loading images etc:
#
# So, like a lot of people I wanted some nice card images
# for the game. However I also wanted to fall back to a basic
# version so the user wouldn't have to wait while the images
# loaded if that took a long time.
#
# So loaded tracks the number of images loaded so far (by checking
# width>0). In new_game() set picture_version to True or False
# depending on whether the images are loaded. This way it won't
# switch versions during a game.
#
# So far, so good but it mean that the first game was always a
# basic one because the images were never loaded. This was true
# even if the browser had them cached (e.g. they'd run the program,
# stopped, run it again). So to allow the images to load from
# cached versions I added the preload timer. This is a timer that
# is triggered once at the beginning and once it fires it starts
# the first game. This however means there's always a short gap
# before the first game can begin. So when in this state I display
# a "please wait" message.
#
# Added to this I tracked the number of pairs the user has and when
# they got them all then display a "you won" message for up to
# five seconds or the user hits reset
#
# This is tracked by program_state - which basically tells draw()
# what to display:
#
#   STATE_PRELOAD  --> "Please wait..."
#   STATE_WON      --> "You Won!"
#   STATE_PLAYING  --> draw cards
#

# initial "Please wait..." period (ms)
PRELOAD_DELAY = 2500
# time to show "you Won!" message (ms)
WIN_PAUSE = 5000

# cards list of numbers 0-7 twice
cards = list(range(8))
cards.extend(list(range(8)))
# empty list for card images
im = []

# list for cards which are exposed
exposed = [False]*16

# helper function to initialize globals
def new_game():
    global cards,game_state, turns, loaded, picture_version
    global pairs, program_state

    # beginning game_state with 0 turns, 0 pairs
    game_state = 0
    turns = 0
    pairs = 0
    turns_lbl.set_text("Turns = "+str(turns))
    pairs_lbl.set_text("Pairs = "+str(pairs))

    # shuffle twice? not really...
    # cards is the list of values,0-7, which we shuffle to get a random board
    # for the "numbers case" this is all we need.
    # For the "pictures" version im is the list of images. We use the cards
    # values as the index into this list but we have 54 images (52+two jokers) so
    # in order to get different cards each time shuffle the images so different
    # cards appear in the first 8
    #
    # TLDR? if we didn't shuffle cards we'd get pairs in predictable places
    #       if we didn't shuffle images we'd get the same 8 cards when we have more
    random.shuffle(cards)
    random.shuffle(im)

    # reset exposed to all False
    for c in range(len(exposed)):
          exposed[c]=False

    # do the picture version if the images are loaded
    if loaded == NUM_IMAGES:
        picture_version = True
    else:
        picture_version = False

    # set state to PLAYING
    program_state = STATE_PLAYING
    # stop the winning timer (user hit reset)
    win_timer.stop()

# win_timer fires WIN_PAUSE after user won and then starts a new game
def win_timer():
    new_game()

# define event handlers
def mouseclick(pos):
    global game_state, card1, card2, turns,pairs, program_state

    #idx is the index of the card we clicked on
    idx = pos[0] // CARD_WIDTH + (pos[1] //CARD_HEIGHT)*4

    #there's no case where clicking an exposed card should do anything so
    # just return
    if exposed[idx]:
        return

    #expose card we just clicked on
    exposed[idx]= True

    if game_state == 0:
        #state 0, new game - record this card as card1 and move to game_state1
        card1 = idx
        game_state = 1
    elif game_state == 1:
        #state 1, single (unpaired) card showing - record this card as card2,
        # move to game_state 2 and update the turns counter (and label)
        card2 = idx
        game_state = 2
        turns += 1
        turns_lbl.set_text("Turns = "+str(turns))
        #if the new card matches then it's a new pair
        if cards[card1] == cards[card2]:
            pairs += 1
            pairs_lbl.set_text("Pairs = "+str(pairs))
            #if it's the last pair then trigger a win
            if pairs == WINNING_PAIRS:
                program_state = STATE_WON
                win_timer.start()
    else:
        #game_state 2, two (unpaired) cards showing
        # - check whether last two cards match, if not then flip them back (exposed = False)
        # - record this card as card1
        # - move to game_state 1
        if cards[card1] != cards[card2]:
            exposed[card1]=False
            exposed[card2]=False

        card1=idx
        game_state = 1

def draw(canvas):
    global cards,im,picture_version
    global program_state

    # STATE_PRELOAD - means we're waiting to load the images - sort of, see
    # comment above. Anyway, whilst in this state we simply show a courtesy
    # message so the user knows something's happening.
    if program_state == STATE_PRELOAD:
        canvas.draw_text("Please wait...",[30,70],20,"White")
        return

    # STATE_WON - user won so display a message saying so
    #  this will last until win_timer fires or user hits
    #  reset
    if program_state == STATE_WON:
        canvas.draw_text("You",[120,175],30,"Red")
        canvas.draw_text("WON!",[100,275],40,"Red")
        return

    # STATE_PLAYING - normal game play
    #draw the cards
    for card in range(len(cards)):
        #co-ordinates of top left of card position, numbering:
        #  0,  1,  2,  3
        #  4,  5,  6,  7
        #  8,  9, 10, 11
        # 12, 13, 14, 15
        card_x = (card % 4) * CARD_WIDTH
        card_y = (card // 4 ) * CARD_HEIGHT

        if exposed[card]:
            #card is showing
            if picture_version:
                 # PICTURE mode - the image appropriate to the card
                canvas.draw_image(im[cards[card]],[CARD_WIDTH/2,CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT],[card_x+CARD_WIDTH/2,card_y+CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT])
            else:
                # NUMBERS mode - white-bordered black rectangle with a white card number in the centre
                canvas.draw_polygon([[card_x,card_y],[card_x+CARD_WIDTH,card_y],[card_x+CARD_WIDTH,card_y+CARD_HEIGHT],[card_x,card_y+CARD_HEIGHT]],2,"White","Black")
                canvas.draw_text(str(cards[card]),[card_x+30,card_y+70],40,"White")
        else:
            #card no showing
            if picture_version:
                 # PICTURES mode - the image for the back of a card
                canvas.draw_image(back_im,[CARD_WIDTH/2,CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT],[card_x+CARD_WIDTH/2,card_y+CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT])
            else:
                # NUMBERS mode - dark blue rectangle bordered in white
                canvas.draw_polygon([[card_x,card_y],[card_x+CARD_WIDTH,card_y],[card_x+CARD_WIDTH,card_y+CARD_HEIGHT],[card_x,card_y+CARD_HEIGHT]],2,"White","darkblue")

# this timer is used to check whether the images have loaded
def load_status_timer():
    global loaded, im, back_im, wait_msg, load_status

    # loaded counts how many images have width > 0 i.e. have successfully loaded
    loaded = 0

    # check back image
    if load_status > NOTHING_LOADED:
        if back_im.get_width() > 0:
            loaded += 1

    # check each card image
    if load_status > BACK_LOADED:
        for i in range(len(im)):
            if im[i].get_width() > 0:
                loaded += 1

    # if all images loaded then stop checking
    if loaded == NUM_IMAGES:
        check_loading_timer.stop()

# a timer to start the first game
def preload_timer():
    initial_timer.stop()
    new_game()

# a timer to load the images
def image_timer():
    global NUM_IMAGES

    image_load_timer.stop()
    load_images()
    NUM_IMAGES += len(im)

# convenience function to load the images
def load_images():
    global im, back_im, load_status

    load_status=NOTHING_LOADED

    # load images
    # back
    back_im=simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWFV1UFFYRWswdDg")
    load_status=BACK_LOADED

    #within each group the suits are in order (Diamonds, Hearts, Clubs, Spades)
    #aces
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmRzI4MnpCdC1GYlU"))
    load_status=IM_LOADED
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmdGU4N1NKa1kyalk"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmbDJ5eG44TnJBQ0U"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWkotYVBHTEdILWs"))
    #twos
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmNURac3h0aUhrdTQ"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmcmwwVzJaRDh4U1k"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmdm11UXplazh2RTg"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmbXVoWXRncnZ4TUk"))
    #threes
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmVlpVRmxyNHVacnM"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmUnNhMzVpRlJlY2s"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmN0JqdFVFaTZTMGM"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmNDdtLV9lejJkYm8"))
    #fours
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmbUhTVjNYMDN6cjg"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmeWVaSU1rUk9HYVk"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmN1FjT05MdE1yS00"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmQTAyNzZDYnNIdk0"))
    #fives
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmcFIza0lzSEZEbDA"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmbnlOMjdicjBqX3M"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmTnMtSUxkTkhBbVU"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmdGtCWC1Ja2M3QlE"))
    #sixes
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmeXRDSUt0aXZPaWs"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmTldlNlBUeUVNZFk"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmQjAwQjRvLUhTQ3M"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmUldFRUsxZWY1SUU"))
    #sevens
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmU2RSdEVZR1pyOWs"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmd0ZQMDdJNkdSV2M"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmcHVReExmTGhxTTQ"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmM0R1WlVTVlYyc0k"))
    #eights
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmcG9WQVQ2ekpXN3c"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmRHJrNTAtNi01QWc"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWTVwWkRha1QtMzQ"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmMGxhQkhoT25aZlE"))
    #nines
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmVXR6UEtfQk9NaVk"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmT0JJNktyYjhld0E"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmanMweVpuZUZGcFU"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmbFUwd2JzVE1UVnM"))

    #tens
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmRDJpdkRSOTQyVHM"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmM3VlU0JiaUhxWkE"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmN1hyZUlZSHlxUnc"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmY1hNLXhXVTZhODA"))

    #jacks
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmQzRRVEV1S3lOZmc"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmbU9EQWhSUzh6TXc"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmNWVheFJBUkZPZE0"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmYUhJSWY4TlRmR0k"))
    #queens
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmTDdBaHRTNzRDTXM"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmVlZ0MEsyVzN2U0U"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmaW9pcmdKaW1IeGM"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmRVdPeGVjOXhGT00"))
    #kings
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWjh5anlXam4wd2s"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmaFRFbzRicHc3RDA"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmOXlCdG85S3dhUVU"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmcUlCRnAtUWREamc"))

    #jokers
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmbm03emdSYVBIazQ"))
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmNTNYSUMwX0tTZ28"))



# create frame and add a button and labels

# frame with canvas for 4x4 cards
frame = simplegui.create_frame("Memory", CARD_WIDTH * 4, CARD_HEIGHT * 4)

# add reset button
frame.add_button("Reset", new_game)
# spacer - can't find a more elegant way to do this
frame.add_label("   ")

# turns label, pairs label
turns_lbl = frame.add_label("Turns = 0")
frame.add_label("   ")
pairs_lbl = frame.add_label("Pairs = 0")
frame.add_label("   ")

#credit where credit's due!
credit = frame.add_label("(card images by Nicu: http://nicubunu.ro/cards/)")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

#start timer to load iamges
image_load_timer = simplegui.create_timer(100,image_timer)
image_load_timer.start()

#start timer to check loading status of images
check_loading_timer = simplegui.create_timer(100,load_status_timer)
check_loading_timer.start()



#start timer for initial game
initial_timer = simplegui.create_timer(PRELOAD_DELAY,preload_timer)
initial_timer.start()

# create but do not start win timer
win_timer = simplegui.create_timer(WIN_PAUSE,win_timer)

#kick things off - start the frame
frame.start()

# Always remember to review the grading rubric