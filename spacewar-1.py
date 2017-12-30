import random
import time
#Import the Turtle module
import turtle
from playsound import playsound



turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
turtle.title("Space War")
turtle.bgpic("spacebg.gif")
turtle.ht()
turtle.setundobuffer(1)
turtle.tracer(0)


#Register the shapes
turtle.register_shape("spaceship7.gif")

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        turtle.Turtle.__init__(self, shape = spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.fd(0)
        self.goto(startx, starty)
        self.speed = 1

    def move(self):
        self.fd(self.speed)

    #Boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other ):
        if(self.xcor() >= (other.xcor() -20)) and \
        (self.xcor() <= (other.xcor() +20)) and \
        (self.ycor() >= (other.ycor() -20)) and \
        (self.ycor() <= (other.ycor() +20)) :
            return True
        else:
            return False

class Player(Sprite):

    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        #self.shape("spaceship7.gif")
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 3
        self.lives = 3

    def turn_left(self):
       self.lt(25)

    def turn_right(self):
        self.rt(25)

    def accelarate(self):
        self.speed +=1

    def decelarate(self):
        self.speed -=1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 4
        self.setheading(random.randint(0,360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)

    #Boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)

class Cannon(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)

    def fire(self):
        if self.status == "ready":
            #Play cannon sound
            playsound('./Laser.wav', False)
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):

        if self.status == "ready":
            self.goto(-1000, 1000)
        if self.status == "firing":
            self.fd(self.speed)

    # Border check
        if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, 1000)

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3

    def draw_border(self):
        #Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))


#Create game object
game = Game()

#Draw the game border
game.draw_border()

#Show the game status
game.show_status()

#Create my sprites
player = Player("triangle", "white", 0, 0)
#enemy = Enemy("circle", "red", -100, 0)
cannon = Cannon("triangle", "yellow", 0, 0)
#ally = Ally("square", "blue", 100, 0)

enemies = []
for i in range(6):
    enemies.append(Enemy("circle", "red", -100, 0))

allies = []
for n in range(4):
    allies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(20):
    particles.append((Particle("circle", "orange", 0, 0)))

#Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelarate, "Up")
turtle.onkey(player.decelarate, "Down")
turtle.onkey(cannon.fire, "space")
turtle.listen()


# Main game loop
while True:
    turtle.update()
    time.sleep(0.02)

    player.move()
    cannon.move()

    for enemy in enemies:
        enemy.move()

        # Check for collision with player
        if player.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 10
            game.show_status()

        # Check for collision between the cannon and the enemy
        if cannon.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            cannon.status = "ready"
            #Increase the score
            game.score +=100
            game.show_status()
            # Do the explosion
            for particle in particles:
                particle.explode(cannon.xcor(), cannon.ycor())


    for ally in allies:
        ally.move()
        # Check for collision between the cannon and the ally
        if cannon.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            cannon.status = "ready"
            #Decrease the score
            game.score -=20
            game.show_status()

    for particle in particles:
        particle.move()


delay = raw_input("Press enter to finish. > ")