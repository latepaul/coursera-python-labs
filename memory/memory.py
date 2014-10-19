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
for c in range(16):
    exposed.append(False)

state = 0
card1 = card2 = -1
turns = 0

# helper function to initialize globals
def new_game():
    global cards,state, turns

    state = 0
    turns = 0

    random.shuffle(cards)
    for c in range(len(exposed)):
          exposed[c]=False

    label.set_text("Turns = "+str(turns))

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, card1, card2, turns

    idx = pos[0] // 50

    if not exposed[idx]:
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
    global cards, im,loaded

    for card in range(len(cards)):
        if exposed[card]:
            canvas.draw_polygon([[card*50,0],[(card+1)*50,0],[(card+1)*50,100],[card*50,100]],2,"White","Black")
            canvas.draw_text(str(cards[card]),[card*50+CARD_XPOS,CARD_YPOS],CARD_FONT,"White")
        else:
            canvas.draw_polygon([[card*50,0],[(card+1)*50,0],[(card+1)*50,100],[card*50,100]],2,"White","Green")

        if loaded:
            canvas.draw_image(im,[100,125],[200,250],[card*50+25,50],[50,100])

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
loaded=False
im = simplegui.load_image("http://images.all-free-download.com/images/graphiclarge/spade_suit_two_playing_cards_311648.jpg")
loaded=True

new_game()
frame.start()


# Always remember to review the grading rubric