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
state = 0
card1 = card2 = -1
turns = 0
pairs = 0
WINNING_PAIRS = 8

# loaded and picture_version are for when images are loading
loaded = 0
picture_version = False
game_started = False
NUM_IMAGES = 1
# initial "Please wait..." period (ms)
PRELOAD_DELAY = 500
wait_message = "Game loading, please wait..."
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
    global cards,state, turns, loaded, picture_version, game_started

    # beginning state with 0 turns
    state = 0
    turns = 0
    turns_lbl.set_text("Turns = "+str(turns))
    pairs_lbl.set_text("Pairs = "+str(pairs))

    # shuffle twice? not really
    # cards is the list of values,0-7, which we shuffle to get a random board
    # for the "numbers case" this is all we need.
    # For the "pictures" version im is the list of images. We use the cards
    # values as the index into this listbut we have 54 images (52+two jokers) so
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

    if loaded == NUM_IMAGES:
        picture_version = True
    else:
        picture_version = False
        
    game_started = True
    win_timer.stop()

def win():
    global wait_message, game_started

    wait_message = "Congratulations you won!"
    game_started = False
    win_timer.start()

def win_timer():
    new_game()

# define event handlers
def mouseclick(pos):
    global state, card1, card2, turns,pairs

    #idx is the index of the card we clicked on
    idx = pos[0] // CARD_WIDTH + (pos[1] //CARD_HEIGHT)*4

    #there's no case where clicking an exposed card should do anything so
    # just return
    if exposed[idx]:
        return

    #expose card we just clicked on
    exposed[idx]= True

    if state == 0:
        #state 0, new game - record this card as card1 and move to state1
        card1 = idx
        state = 1
    elif state == 1:
        #state 1, single (unpaired) card showing - record this card as card2,
        # move to state 2 and update the turns counter (and label)
        card2 = idx
        state = 2
        turns += 1
        turns_lbl.set_text("Turns = "+str(turns))
        if cards[card1] == cards[card2]:
            pairs += 1
            pairs_lbl.set_text("Pairs = "+str(pairs))
            if pairs == WINNING_PAIRS:
                win()
    else:
        #state 2, two (unpaired) cards showing
        # - check whether last two cards match, if not then flip them back (exposed = False)
        # - record this card as card1
        # - move to state 1
        if cards[card1] != cards[card2]:
            exposed[card1]=False
            exposed[card2]=False
        
        card1=idx
        state = 1

def draw(canvas):
    global cards,im,picture_version
    global game_started

    if not game_started:
        canvas.draw_text(wait_message,[30,70],20,"White")
        return
    
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
    global loaded, im, back_im, wait_msg

    # loaded counts how many images have width > 0 i.e. have successfully loaded
    loaded = 0

    if back_im.get_width() > 0:
        loaded += 1

    for i in range(len(im)):
        if im[i].get_width() > 0:
            loaded += 1

    if loaded == NUM_IMAGES:
        check_loading_timer.stop()

def preload_timer():

    initial_timer.stop()
    new_game()
    
def load_images():
    global im, back_im

    # load images
    # back
    back_im=simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWFV1UFFYRWswdDg")

    #in order (Diamonds, Hearts, Clubs, Spades)
    #aces
    im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmRzI4MnpCdC1GYlU"))
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

# turns label, switch game type button
turns_lbl = frame.add_label("Turns = 0")
frame.add_label("   ")
frame.add_label("   ")
pairs_lbl = frame.add_label("Pairs = 0")
frame.add_label("   ")
frame.add_label("   ")

#credit where credit's due!
credit = frame.add_label("(card images by Nicu: http://nicubunu.ro/cards/)")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


load_images()
NUM_IMAGES += len(im)

#start timer to check loading status of images
check_loading_timer = simplegui.create_timer(100,load_status_timer)
check_loading_timer.start()

initial_timer = simplegui.create_timer(500,preload_timer)
initial_timer.start()

win_timer = simplegui.create_timer(WIN_PAUSE,win_timer)

#kick things off
frame.start()

# Always remember to review the grading rubric