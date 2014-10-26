# implementation of card game - Memory
# Codeskulptor URL:

try:
    import simplegui
except:
    import simpleguitk as simplegui

# card size
CARD_SIZE = (88,120)
TILE_SIZE = (72,96)
BIG_IMAGE_SIZE = (936,480)

CLUBS = 0
SPADES = 1
HEARTS = 2
DIAMONDS = 3
JOKER = 4
SUIT_DICT = { CLUBS:2,SPADES:3,HEARTS:1,DIAMONDS:0, JOKER:4}

# empty list for card images
im = []
first = True

def draw(canvas):
    global im,first

    for suit in range(5):
        suit_im_idx = SUIT_DICT[suit]
        if first:
            print "Suit:",suit,"idx:",suit_im_idx
        
        for card in range(13):
            if suit == JOKER:
                if card % 3 == 2:
                    if first:
                        print " suit:",suit,"card:",card," back"
                    this_im = back_im
                else:
                    if first:
                        print " suit:",suit,"card:",card," joker",card %2
                    this_im = im[52 + (card % 2)]
            else:
                if first:
                        print " suit:",suit,"card:",card," overall idx",(card*13 + suit_im_idx)
                this_im = im[(card * 4)+ suit_im_idx]
            canvas.draw_image(this_im, [CARD_SIZE[0]/2,CARD_SIZE[1]/2],CARD_SIZE,[TILE_SIZE[0]*card + TILE_SIZE[0]/2,TILE_SIZE[1]*suit + TILE_SIZE[1]/2],TILE_SIZE)
    if first:
        first = False

# convenience function to load the images
def load_images():
    global im, back_im

    # load images
    # back
    back_im=simplegui.load_image("https://docs.google.com/uc?export=download&id=0B4HFB7ccwbPmWFV1UFFYRWswdDg")

    #within each group the suits are in order (Diamonds, Hearts, Clubs, Spades)
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
frame = simplegui.create_frame("Tiler", BIG_IMAGE_SIZE[0],BIG_IMAGE_SIZE[1])
frame.set_canvas_background("white")
#credit where credit's due!
credit = frame.add_label("(card images by Nicu: http://nicubunu.ro/cards/)")

# load the images
load_images()
frame.set_draw_handler(draw)
#kick things off - start the frame
frame.start()
