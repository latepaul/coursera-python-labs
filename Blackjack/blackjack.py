# Mini-project #6 - Blackjack

try:
    import simplegui
except:
    import simpleguitk as simplegui

import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

#Nicu images version
# card_images = simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmS0tzZTRBZkNwcXc")
# card_back=simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWFV1UFFYRWswdDg")
# CARD_BACK_SIZE = (88, 120)
# CARD_BACK_CENTER = (44, 60)


# initialize some useful global variables
in_play = False
outcome = ""
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
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
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
        pass	# draw a hand on the canvas, use the draw method for cards


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
    global outcome, in_play, dealer_hand, player_hand, deck

    # your code goes here
    print "Dealing..."
    deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "Dealer has:",str(dealer_hand),"(",dealer_hand.get_value(),")"
    print "Player has:",str(player_hand),"(",player_hand.get_value(),")"
    in_play = True

def hit():
    global score

    # if the hand is in play, hit the player
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        print "Player now has:",str(player_hand),"(",player_hand.get_value(),")"

    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() > 21:
        print "You have busted!"

    if player_hand.get_value() == 21 and dealer_hand.get_value() == 21:
        print "Bad luck! Dealer wins tie at 21!!"

def stand():
    global score

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    if player_hand.get_value() > 21:
        print "You busted, remember!"
        return

    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
        print "Dealer now has:",str(dealer_hand),"(",dealer_hand.get_value(),")"

    if dealer_hand.get_value() > 21:
        print "Dealer has busted",dealer_hand.get_value()

    # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() >= player_hand.get_value():
        print "Dealer wins!"
    else:
        print "Player wins!"
    print "Dealer :",dealer_hand.get_value()," vs Player :",player_hand.get_value()

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below

    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deck = Deck()
# get things rolling
deal()
frame.start()


# remember to review the gradic rubric