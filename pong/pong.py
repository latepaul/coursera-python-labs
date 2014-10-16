# Implementation of classic arcade game Pong

# Codeskulptor URL: http://www.codeskulptor.org/#user38_b7FXxGRalqHjlN9.py

# colours, font sizes etc are tuned to Codeskulptor's output!!

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

#Position of right hand gutter
RGUTTER=WIDTH - 1 - PAD_WIDTH

LEFT = False
RIGHT = True

#position for scores
LSCORE_POS = WIDTH/4 - 24
RSCORE_POS = (WIDTH/4)*3

PADDLE_SPEED = 3


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    # create random velocity as per instructions. However the 
    # suggested values are pixel/second and we will use these in draw()
    # which gets called 60 times a second so adjust accordingly
    vel_hor = float(random.randrange(120, 240)/60.0)
    vel_vert = float(random.randrange(60, 180)/60.0)
    
    if direction == RIGHT:
        ball_vel = [vel_hor,-vel_vert]
    else:
        ball_vel = [-vel_hor,-vel_vert]

    #initial ball position is the centre of the screen
    ball_pos = [WIDTH/2,(HEIGHT/2)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global rally,rally_hi

    #initial ball for game is randomly left or right    
    if random.randint(0,9) > 5:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

    # set initial paddle positions, velocities and scores
    paddle1_pos = paddle2_pos = HEIGHT/2
    paddle1_vel = paddle2_vel = 0
    score1 = score2 = 0
    
    #used to track rallys
    rally_hi = rally = 0

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle1_vel, rally,rally_hi

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    #bounce off top and bottom
    if ball_pos[1] > HEIGHT-1-BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
        ball_pos[1] = HEIGHT-1-BALL_RADIUS

    if ball_pos[1] < BALL_RADIUS:
        ball_pos[1] = BALL_RADIUS
        ball_vel[1]=-ball_vel[1]

    #test for collision with gutter/paddle
    #left gutter/player1
    if ball_pos[0] < BALL_RADIUS+PAD_WIDTH:
        #inside gutter line, are we hitting the paddle?
        if ball_pos[1] > paddle1_pos -HALF_PAD_HEIGHT-BALL_RADIUS and ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT+BALL_RADIUS:
            #paddle so change ball direction, increase speed and increment rally count
            ball_vel[0]=-ball_vel[0]
            ball_pos[0]=BALL_RADIUS+PAD_WIDTH
            ball_vel[0]=1.1*ball_vel[0]
            ball_vel[1]=1.1*ball_vel[1]
            rally += 1
            if rally > rally_hi:
                rally_hi=rally
        else:
            score2 += 1
            rally = 0
            spawn_ball(RIGHT)
    #right gutter/player2    
    if ball_pos[0] > WIDTH - 1 - BALL_RADIUS-PAD_WIDTH:
        if ball_pos[1] > paddle2_pos -HALF_PAD_HEIGHT-BALL_RADIUS and ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT+BALL_RADIUS:
            ball_vel[0]=-ball_vel[0]
            ball_pos[0]=WIDTH - 1 -BALL_RADIUS- PAD_WIDTH
            ball_vel[0]=1.1*ball_vel[0]
            ball_vel[1]=1.1*ball_vel[1]
            rally += 1
            if rally > rally_hi:
                rally_hi=rally
        else:
            score1 += 1
            rally = 0
            spawn_ball(LEFT)


    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,"White","WHITE")

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel > HALF_PAD_HEIGHT and paddle1_pos + paddle1_vel < HEIGHT - 1 - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel
        
    if paddle2_pos + paddle2_vel > HALF_PAD_HEIGHT and paddle2_pos + paddle2_vel < HEIGHT - 1 - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel

    # draw paddles
    pad_top=paddle1_pos+HALF_PAD_HEIGHT
    pad_bot=paddle1_pos-HALF_PAD_HEIGHT
    canvas.draw_polygon([[0,pad_top],[PAD_WIDTH,pad_top], [PAD_WIDTH,pad_bot],[0,pad_bot]],2,"white","red")

    pad_top=paddle2_pos+HALF_PAD_HEIGHT
    pad_bot=paddle2_pos-HALF_PAD_HEIGHT
    canvas.draw_polygon([[RGUTTER,pad_top],[WIDTH-1,pad_top], [WIDTH-1,pad_bot],[RGUTTER,pad_bot]],2,"white","green")
    
    # draw scores
    canvas.draw_text(str(score1),[LSCORE_POS,BALL_RADIUS*2],40,"Red")
    canvas.draw_text(str(score2),[RSCORE_POS,BALL_RADIUS*2],40,"Green")
    canvas.draw_text('Rally:'+str(rally),[WIDTH-100,HEIGHT - 25],26,"Orange")
    canvas.draw_text('High:'+str(rally_hi),[WIDTH-100,HEIGHT - 5],26,"Orange")


def keydown(key):
    global paddle1_vel, paddle2_vel

    # check which key was pressed
    # note because of the order of this if the paddle should
    # go up if the up&down keys or w&s keys are pressed at the same time
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -PADDLE_SPEED
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = PADDLE_SPEED
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = -PADDLE_SPEED
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = PADDLE_SPEED

def keyup(key):
    global paddle1_vel, paddle2_vel

    # depending on which key was released stop either the 
    # player1 or player2's paddle
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart',new_game,100)

# start frame
new_game()
frame.start()
