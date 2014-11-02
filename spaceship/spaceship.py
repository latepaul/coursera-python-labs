# program template for Spaceship
try:
    import simplegui
except:
    import simpleguitk as simplegui

import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

ANG_VEC_CHANGE = 0.05
ACC_CONST = 0.3
FRICTION_CONST = 0.05
MIS_ACC = 4

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
# ship's radius - assume ship is inscribed inside a circle
ship_radius = ship_info.size[0]/2

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        if self.thrust:
            thrust_center = [self.image_center[0]+self.image_size[0],self.image_center[1]]
            canvas.draw_image(self.image,thrust_center,self.image_size,self.pos,self.image_size,self.angle)
        else:
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
                

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        
        self.vel[0] *= (1 - FRICTION_CONST)
        self.vel[1] *= (1 - FRICTION_CONST)
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += ACC_CONST * forward[0]
            self.vel[1] += ACC_CONST * forward[1]
            
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        
    def dec_angvel(self):
        self.angle_vel -= ANG_VEC_CHANGE

    def inc_angvel(self):
        self.angle_vel += ANG_VEC_CHANGE
        
    def set_thrust(self,thrust):
        self.thrust = thrust
        if thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global a_missile, ship_radius
        
        mis_vel = [self.vel[0],self.vel[1]]
        cannon = angle_to_vector(self.angle)
        mis_vel[0] += MIS_ACC*cannon[0]
        mis_vel[1] += MIS_ACC*cannon[1]
        cannon[0] *= ship_radius
        cannon[1] *= ship_radius
        cannon[0] += self.pos[0]
        cannon[1] += self.pos[1]
        a_missile = Sprite(cannon, mis_vel, 0, 0, missile_image, missile_info, missile_sound)        


# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT

def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
#    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
#    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
#    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    
    a_rock = Sprite([random.randrange(0,WIDTH), random.randrange(0,HEIGHT)], [random.random()*2.5-1.25, random.random()*2.5-1.25], 0, (random.random()-0.5)*0.3, asteroid_image, asteroid_info)

def ship_left():
    my_ship.dec_angvel()
    
def ship_right():
    my_ship.inc_angvel()

def thrust_on():
    my_ship.set_thrust(True)

def thrust_off():
    my_ship.set_thrust(False)
    
def shoot():
    my_ship.shoot()
    
def nowt():
    pass
    
KEY_ACTIONS = {'left':[ship_left,ship_right],'right':[ship_right,ship_left], 'up': [thrust_on,thrust_off],'space':[shoot,nowt]}


#key down
def keydown(key):

    for k in KEY_ACTIONS:
        if key == simplegui.KEY_MAP[k]:
           KEY_ACTIONS[k][0]()

def keyup(key):

    for k in KEY_ACTIONS:
        if key == simplegui.KEY_MAP[k]:
            KEY_ACTIONS[k][1]()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [-0.25, -0.1], 1, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, -0.05, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
