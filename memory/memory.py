# implementation of card game - Memory
# Codeskulptor URL:

# allow use in CodeSkulptor or regular python with simpleguitk
try:
    import simplegui
    codeskulptor=True
except:
    import simpleguitk as simplegui
    codeskulptor=False

import random

if codeskulptor:
    CARD_FONT = 40
    CARD_XPOS = 10
    CARD_YPOS = 63
else:
    CARD_FONT = 24
    CARD_XPOS = 20
    CARD_YPOS = 70

cards = list(range(8))
cards.extend(list(range(8)))
exposed = []
im = []
for c in range(16):
    exposed.append(False)

state = 0
card1 = card2 = -1
turns = 0
PICTURES = False
NUMBERS = True
card_set = NUMBERS

# helper function to initialize globals
def new_game():
    global cards,state, turns

    state = 0
    turns = 0

    random.shuffle(cards)
    for c in range(len(exposed)):
          exposed[c]=False

    label.set_text("Turns = "+str(turns))

def switch_sets():
    global card_set, sw_button
    
    if card_set == PICTURES:
        card_set = NUMBERS
        sw_button.set_text("Pictures")
    else:
        card_set = PICTURES
        sw_button.set_text("Numbers")
        
    new_game()
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card1, card2, turns

    idx = pos[0] // 50
    if exposed[idx]:
        return    

    exposed[idx]= True
        
    if state == 0:
        card1 = idx
        state = 1
    elif state == 1:
        card2 = idx
        state = 2
        turns += 1
    else:
        if cards[card1] != cards[card2]:
                exposed[card1]=False
                exposed[card2]=False
        card1=idx
        state = 1

    label.set_text("Turns = "+str(turns))

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global cards, im,loaded, card_set

    if card_set == PICTURES and not loaded:
        canvas.draw_text("PLEASE WAIT WHILE IMAGES LOAD",[10,50],CARD_FONT,"Orange")
        return
        
    for card in range(len(cards)):
        if exposed[card]:
            if card_set == NUMBERS:
                canvas.draw_polygon([[card*50,0],[(card+1)*50,0],[(card+1)*50,100],[card*50,100]],2,"White","Black")
                canvas.draw_text(str(cards[card]),[card*50+CARD_XPOS,CARD_YPOS],CARD_FONT,"White")
            else:
                canvas.draw_image(im[cards[card]],[44,60],[88,120],[card*50+25,50],[50,100])
        else:
            if card_set == NUMBERS:
                canvas.draw_polygon([[card*50,0],[(card+1)*50,0],[(card+1)*50,100],[card*50,100]],2,"White","Green")
            else:
                canvas.draw_image(back_im,[44,60],[88,120],[card*50+25,50],[50,100])
                

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
sw_button = frame.add_button("Pictures", switch_sets)

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
loaded=False

back_im=simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWFV1UFFYRWswdDg")
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

random.shuffle(im)
loaded=True

new_game()
frame.start()


# Always remember to review the grading rubric