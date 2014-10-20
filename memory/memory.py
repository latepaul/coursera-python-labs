# implementation of card game - Memory
# Codeskulptor URL:

import simpleguitk as simplegui
import random

# constants
# card size
CARD_WIDTH = 88
CARD_HEIGHT = 120

# card types
PICTURES = False
NUMBERS = True
# dictionary of "switch button" labels
SET_BUTTON = { NUMBERS : "Picture Cards", PICTURES : "Simple" }

# global variables
# game play variables
state = 0
card1 = card2 = -1
turns = 0

# loaded and wait_msg are for when images are loading
loaded = 0
wait_msg = "00%"
# default to fancy image version
card_set = PICTURES

# default to first of 3 sets
chosen_back = 0

# lists
# cards list of numbers 0-7 twice
cards = list(range(8))
cards.extend(list(range(8)))
# empty list for card images
im = []
back_im = []

# list for cards which are exposed 
exposed = [False for x in range(16)]

# helper function to initialize globals
def new_game():
    global cards,state, turns

    # beginning state with 0 turns
    state = 0
    turns = 0
    label.set_text("Turns = "+str(turns))
 
    # shuffle twice? not really
    # cards is the list of values, which we shuffle to get a random board
    # im is the list of images. We use the cards values as the index to this list
    # and we have 16 card images but we only need 8 (pairs) so shuffle so that we
    # get different cards each time
    # (If I'd had the patience to upload them all there would be 52 card images!)
    random.shuffle(cards)
    random.shuffle(im)
    
    # reset exposed to all False
    for c in range(len(exposed)):
          exposed[c]=False

def switch_sets():
    global card_set, sw_button
    
    #swap between game types
    card_set = not card_set
    sw_button.set_text(SET_BUTTON[card_set])      
    
    #I suppose technically I don't need to start a new game when swapping but
    #since I used the card value as the index, if I didn't then a Jack would become
    #a 0, an ace a 1 etc - and not even be consistent amongst games!
    #starting a new game hides that from the user
    new_game()
    
#new_back detects whether we clicked on a back cover image
# it returns 0,1,2 if we did - corresponding to the back cover image no
# if we clicked on the normal board it returns -1
# otherwise it returns -2
def new_back(click_pos):
    
    #anywhere to the left of 4 card widths is the normal playing board
    if click_pos[0] < CARD_WIDTH*4:
        return -1
    
    #in numbers mode ignore clicks not on the normal board
    if card_set == NUMBERS:
        return -2
    
    #is the click within the left, right range for the mini backs?
    if click_pos[0] >= 4*CARD_WIDTH + 20 and click_pos[0] <= 4.67*CARD_WIDTH + 20:
        #check each back and if the click was in that vertical position return its index value
        for back in range(3):
            back_ytop = 75 + back * CARD_HEIGHT 
            back_ybot = back_ytop + CARD_HEIGHT*0.67
            if click_pos[1] >= back_ytop and click_pos[1] <= back_ybot:
                return back
            
    #all other cases are ignoreable clicks
    return -2

# define event handlers
def mouseclick(pos):
    global state, card1, card2, turns, chosen_back    

    #check whether user wants to change card backs
    back_no = new_back(pos)
    #if so then change and return (nothing else to do)
    if back_no >= 0:
        chosen_back = back_no
        return
    
    #if they clicked outside normal board then return
    if back_no == -2:
        return
    
    #idx is the index of the card we clicked on
    idx = pos[0] // 88 + (pos[1] //120)*4

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
        label.set_text("Turns = "+str(turns))
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
    global cards,im,loaded, card_set

    # if we're in PICTURES mode and not all the images are loaded yet then
    # display a message so the user knows it's not just stalled
    if card_set == PICTURES and loaded < 19:
        canvas.draw_text("Please wait for",[105,60],40,"orange")
        canvas.draw_text("images to load",[105,120],40,"orange")
        canvas.draw_text(wait_msg,[175,275],40,"Red")
        canvas.draw_text("(or click simple",[115,400],24,"orange")
        canvas.draw_text("for game without images)",[120,425],24,"orange")
        return
        
    #draw a line separating play area to control area
    canvas.draw_line([CARD_WIDTH*4+10,10],[CARD_WIDTH*4+10,CARD_HEIGHT*4 - 10],2,"White")
    
    # draw mini versions of card backs
    if card_set == PICTURES:
        back_x = 4.33*CARD_WIDTH + 20 
        for back in range(3):
            back_y = 75 + (back +0.33) * CARD_HEIGHT 
            canvas.draw_image(back_im[back],[CARD_WIDTH/2,CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT],[back_x,back_y],[CARD_WIDTH*0.67,CARD_HEIGHT*0.67])
    
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
            if card_set == NUMBERS:
                # NUMBERS mode - white-bordered black rectangle with a white card number in the centre
                canvas.draw_polygon([[card_x,card_y],[card_x+CARD_WIDTH,card_y],[card_x+CARD_WIDTH,card_y+CARD_HEIGHT],[card_x,card_y+CARD_HEIGHT]],2,"White","Black")
                canvas.draw_text(str(cards[card]),[card_x+30,card_y+70],40,"White")
            else:
                # PICTURE mode - the image appropriate to the card
                canvas.draw_image(im[cards[card]],[CARD_WIDTH/2,CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT],[card_x+CARD_WIDTH/2,card_y+CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT])
        else:
            #card no showing
            if card_set == NUMBERS:
                # NUMBERS mode - dark blue rectangle bordered in white
                canvas.draw_polygon([[card_x,card_y],[card_x+CARD_WIDTH,card_y],[card_x+CARD_WIDTH,card_y+CARD_HEIGHT],[card_x,card_y+CARD_HEIGHT]],2,"White","darkblue")
            else:
                # PICTURES mode - the image for the back of a card
                canvas.draw_image(back_im[chosen_back],[CARD_WIDTH/2,CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT],[card_x+CARD_WIDTH/2,card_y+CARD_HEIGHT/2],[CARD_WIDTH,CARD_HEIGHT])
    
# this timer is used to check whether the images have loaded
def load_status_timer():
    global loaded, im, back_im, wait_msg
    
    # loaded counts how many images have width > 0 i.e. have successfully loaded
    loaded = 0
    
    for i in range(len(back_im)):
        if back_im[i].get_width() > 0:
            loaded += 1
            
    for i in range(len(im)):
        if im[i].get_width() > 0:
            loaded += 1
            
    # make message text for percentage done
    perc = (loaded * 100) /19
    wait_msg = str(perc)+"%"
    if perc < 10:
        wait_msg = "0" + wait_msg
           
    # if all messages are loaded, stop timer
    if loaded == 19:
        check_loading_timer.stop()
        
# create frame and add a button and labels

# frame with canvas for 4x4 cards
frame = simplegui.create_frame("Memory", CARD_WIDTH * 5, CARD_HEIGHT * 4)

# add reset button
frame.add_button("Reset", new_game)
# spacer - can't find a more elegant way to do this
frame.add_label("   ")

# turns label, switch game type button
label = frame.add_label("Turns = 0")
frame.add_label("   ")
sw_button = frame.add_button(SET_BUTTON[card_set], switch_sets,100)
frame.add_label("   ")

#credit where credit's due!
credit = frame.add_label("(card images by Nicu: http://nicubunu.ro/cards/)")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# load images
# backs
back_im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWFV1UFFYRWswdDg"))
back_im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmOEFCakJzd3lmOW8"))
back_im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmZ25QaWx1XzZ0RGM"))
    
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

#aces
im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmRzI4MnpCdC1GYlU"))
im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmdGU4N1NKa1kyalk"))
im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmbDJ5eG44TnJBQ0U"))
im.append(simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWkotYVBHTEdILWs"))

#start timer to check loading status of images
check_loading_timer = simplegui.create_timer(100,load_status_timer)
check_loading_timer.start()

#kick things off
new_game()
frame.start()

# Always remember to review the grading rubric