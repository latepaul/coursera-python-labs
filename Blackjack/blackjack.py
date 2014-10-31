# Mini-project #6 - Blackjack

try:
    import simplegui
except:
    import simpleguitk as simplegui

import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
# card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
#
# CARD_BACK_SIZE = (72, 96)
# CARD_BACK_CENTER = (36, 48)
# card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

#Nicu images version
card_images = simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmSU5kZUI4c2dqc0k")
card_back=simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWFV1UFFYRWswdDg")
CARD_BACK_SIZE = (88, 120)
CARD_BACK_CENTER = (44, 60)
TABLE_WIDTH = 600
TABLE_HEIGHT = 600
old_x=-99
# initialize some useful global variables
in_play = False

SHORT_MESSAGE_TIME = 5000
NEW_DEAL_MESSAGE = "Press Deal for new game"
HIT_STAND_MESSAGE = "Hit or Stand?"

display_message = HIT_STAND_MESSAGE
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit)-1)
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []


    def __str__(self):
        ret_str='Hand:'
        for c in self.cards:
            ret_str += ' '+str(c)
        return ret_str

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        ret_val = 0
        aces = False
        for card in self.cards:
            ret_val += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                aces = True

        if aces:
            if ret_val + 10 <= 21:
                ret_val += 10

        return ret_val

    def draw(self, canvas, pos):

        i=0
        space = TABLE_WIDTH - pos[0]
        dist_apart = CARD_SIZE[0] + 25
        fit_cards = (space // dist_apart)
        if len(self.cards) > fit_cards:
            dist_apart = (space - 75) // len(self.cards)

        for card in self.cards:
            card.draw(canvas,[pos[0]+i*dist_apart,pos[1]])
            i += 1


# define deck class
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))

    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def __str__(self):
        ret_str = 'Deck contains'
        for card in self.cards:
            ret_str += ' '+str(card)
        return ret_str


#define event handlers for buttons
def deal():
    global in_play, dealer_hand, player_hand, deck, score, display_message


    # your code goes here
    print "Dealing..."
    deck = Deck()
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "Dealer has:",str(dealer_hand),"(",dealer_hand.get_value(),")"
    print "Player has:",str(player_hand),"(",player_hand.get_value(),")"
    display_message = HIT_STAND_MESSAGE
    if in_play:
        short_message("Discarding game, you lose!")
        score -= 1
    in_play = True

def hit():
    global score, in_play

    # if the hand is in play, hit the player
    if not in_play:
        return

    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        print "Player now has:",str(player_hand),"(",player_hand.get_value(),")"

    # if busted, assign a message to display, update in_play and score
    if player_hand.get_value() > 21:
        print "You busted (",player_hand.get_value(),")"
        short_message( "You have busted!")
        in_play = False
        score -= 1

    if player_hand.get_value() == 21 and dealer_hand.get_value() == 21:
        print "Bad luck! Dealer wins tie at 21!!"
        short_message("Bad luck! Dealer wins tie at 21!!")
        in_play = False
        score -= 1

def stand():
    global score, in_play

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if not in_play:
        return

    if player_hand.get_value() > 21:
        print "You busted, remember!"
        short_message("You're busted")
        in_play=False
        return

    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
        print "Dealer now has:",str(dealer_hand),"(",dealer_hand.get_value(),")"

    if dealer_hand.get_value() > 21:
        print "Dealer has busted",dealer_hand.get_value()
        short_message("Dealer has busted")
        in_play = False
        score += 1
        return

    # assign a message to display, update in_play and score
    if dealer_hand.get_value() >= player_hand.get_value():
        print "Dealer wins!"
        short_message("Dealer Wins!")
        score -= 1
    else:
        print "Player wins!"
        short_message("You Won!")
        score += 1
    print "Dealer :",dealer_hand.get_value()," vs Player :",player_hand.get_value()
    in_play = False

def short_term_msg_timer():
    global display_message
    
    # revert to long term message
    if in_play:
        display_message = HIT_STAND_MESSAGE
    else:
        display_message = NEW_DEAL_MESSAGE
        
    short_term_timer.stop()
    print "Back to long term message:", display_message
    
def short_message(message_text):
    global display_message

    print "Short message, setting to:",message_text
    display_message = message_text
    short_term_timer.start()
    
# draw handler
def draw(canvas):
    global display_message,old_x
    # test to make sure that card.draw works, replace with your code below

    player_hand.draw(canvas,[50,400])
    dealer_hand.draw(canvas,[50,200])
    canvas.draw_text("Dealer:",[10,180],20,"White")
    canvas.draw_text("Player:",[10,380],20,"White")
    canvas.draw_text("BLACKJACK",[70,100],60,"Yellow")
    canvas.draw_text("Score:",[470,150],18,"White")
    if score < 0:
        canvas.draw_text(str(score),[550,150],18,"Red")
    else:
        canvas.draw_text(str(score),[550,150],18,"Blue")

    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [50 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE)

    x = 30 + (22 - len(display_message))*10.5
    if old_x != x:
        print "char count=",len(display_message),"x=",x
    old_x=x
    canvas.draw_text(display_message,[x,585],40,"White")

    canvas.draw_polygon([[30,520],[570,520],[570,590],[30,590]],5,"White")

# initialization frame
frame = simplegui.create_frame("Blackjack", TABLE_WIDTH, TABLE_HEIGHT)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label("   ")

#credit where credit's due!
credit = frame.add_label("(card images by Nicu: http://nicubunu.ro/cards/)")

frame.set_draw_handler(draw)

short_term_timer = simplegui.create_timer(SHORT_MESSAGE_TIME, short_term_msg_timer)

deck = Deck()
# get things rolling
deal()
frame.start()


# remember to review the gradic rubric