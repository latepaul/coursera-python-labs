# template for "Stopwatch: The Game"
# http://www.codeskulptor.org/#user38_jydbTAZo6f7K2S6.py
import simplegui

# define global variables

# value for stopwatch counter
timer_value = 0

# timer interval (should we ever wish to change it)
interval = 100

# variables to track the game element
tries = 0
successes = 0

#score is a string displaying game score
#score_x is x position to display it at
score = "0/0"
score_x = 270

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):

    # break time down into elements
    minutes = t // 600
    seconds = (t % 600) // 10
    tenths = (t % 600) - (seconds * 10)

    #add leading zero for single digit seconds
    secs_str = str(seconds)
    if seconds < 10:
        secs_str = "0"+secs_str

    #rubric says behaviour after ten minutes is programmer's choice
    #my choice is to have it wrap around to 0:00.0
    #easiest way to do this is change minutes to 0
    if minutes > 9:
        minutes = 0

    return str(minutes)+':'+secs_str+'.'+str(tenths)

#update the score - both the string used and where it goes
def update_score():
    global score, score_x

    score = str(successes)+"/"+str(tries)

    #update score_x so that the score always aligns to the same right position
    #meaning it doesn't go off the screen
    score_x=300 - (10*len(score))

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    timer.start()

def stop_handler():
    global tries, successes

    # instructions suggest using a boolean but reading the docs shows
    # that a timer has an is_running() property so I'm using that as it's
    # set up and maintained for us

    # so, only count as a "guess" if timer is running
    if timer.is_running():
        tries = tries + 1

        # a win is when we hit X:XX.0 exactly
        if timer_value % 10 == 0:
            successes = successes + 1

        #update the score here as we don't want/need to do it
        #10 or 60 times a second
        update_score()

    #do this last, otherwise is_running() would always be false above!
    timer.stop()

def reset_handler():
    global timer_value, tries, successes

    #reset is simple, stop the timer and reset all the values
    timer.stop()
    timer_value = 0
    tries = 0
    successes = 0

    #update the score - otherwise we won't see it change until
    #our next guess
    update_score()

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global timer_value
    timer_value = timer_value + 1

# define draw handler
def draw_handler(canvas):
    global score_x, score

    #draw the timer and the score
    canvas.draw_text(format(timer_value),[100,150],42,"White")
    canvas.draw_text(score,[score_x,30],18,"Red")

# create frame
frame = simplegui.create_frame("Stopwatch", 300,300)

frame.add_button("Start",start_handler,100)
frame.add_button("Stop",stop_handler,100)
frame.add_button("Reset",reset_handler,100)

# register event handlers
frame.set_draw_handler(draw_handler)

timer = simplegui.create_timer(interval,timer_handler)


# start frame
frame.start()

# Please remember to review the grading rubric
