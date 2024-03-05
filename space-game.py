import os
import random
import time

#import the turtle module
import turtle
turtle.fd(0)
turtle.speed(0)#animation speed
turtle.bgcolor("black")
turtle.title("Space war")
turtle.ht()#hide defualt turtle
turtle.setundobuffer(1)#save memory
turtle.tracer(0)

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

        #boundary detection
        if self.xcor() > 490:
            self.setx(490)
            self.rt(60)
        if self.xcor() < -490:
            self.setx(-490)
            self.rt(60)
        if self.ycor() > 490:
            self.sety(490)
            self.rt(60)
        if self.ycor() < -490:
            self.sety(-490)
            self.rt(60)

    def is_collision(self, other):
        if(self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)) and \
        (self.ycor() <= (other.ycor() + 20)):
            return True
        else:
            return False
        

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=.6, stretch_len=1.1, outline=None)
        self.speed = .3
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed +=.2

    def decelerate(self):
        self.speed -=.2

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = .5
        self.setheading(random.randint(0,360))

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline = None)
        self.speed = 3
        self.status = "ready"
        self.goto(-1000,1000)

    def fire(self):
        if self.status == "ready":
            self.goto(player.xcor(),player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):

        if self.status == "ready":
            self.goto(-1000,1000)

        if self.status == "firing":
            self.fd(self.speed)

        #border check
        if self.xcor() < -490 or self.xcor() > 490 or self.ycor() < -490 or self.ycor() > 490:
            self.goto(-1000, 1000)
            self.status = "ready"

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.speed = .8
        self.setheading(random.randint(0,360))

    def move(self):
        self.fd(self.speed)

        #boundary detection
        if self.xcor() > 490:
            self.setx(490)
            self.lt(60)
        if self.xcor() < -490:
            self.setx(-490)
            self.lt(60)
        if self.ycor() > 490:
            self.sety(490)
            self.lt(60)
        if self.ycor() < -490:
            self.sety(-490)
            self.lt(60)

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        Sprite.__init__(self, spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline = None)
        self.goto(-1000,-1000)
        self.frame=0

    def explode(self, startx, starty):
        self.goto(startx,starty)
        self.setheading(random.randint(0,360))
        self.frame = 1


    def move(self):
        if self.frame != 0:
            self.fd(18-self.frame)
            self.frame += 1

        if self.frame < 6:
            self.shapesize(stretch_wid=0.3, stretch_len=0.3, outline=None)
        elif self.frame < 11:
            self.shapesize(stretch_wid=0.2, stretch_len=0.2, outline=None)
        else:
            self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
			

        if self.frame > 20:
            self.frame = 0
            self.goto(-1000,-1000) 

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
        self.pen.goto(-500,500)
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(1000)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-500, 510)
        self.pen.write(msg, font=("Arial", 16, "normal"))

#Create game object
game = Game()

#Draw border
game.draw_border()

#Show the game status
game.show_status()

#Create my sprites
player = Player("triangle", "white", 0,0)
missile = Missile("circle", "yellow", 0, 0)
allies=[]
for i in range(6):
    allies.append(Ally("square", "blue", 100, 0))

enimies=[]
for i in range(6):
    enimies.append(Enemy("circle", "red", -100, 0))

particles=[]
for i in range(20):
    particles.append(Particle("circle", "orange",0,0))

#keyboard binding
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()



#Main game loop
while True:
    turtle.update()

    player.move()
    missile.move()


    #enimies
    for enemy in enimies:
        enemy.move()

        #Check for collision with enemy
        if player.is_collision(enemy):
            x=random.randint(-450,450)
            y=random.randint(-450,450)
            enemy.goto(x,y)
            game.score -= 100
            game.show_status()

        #Check for missile hit enemy
        if missile.is_collision(enemy):
            x=random.randint(-450,450)
            y=random.randint(-450,450)
            enemy.goto(x,y)
            missile.status = "ready"
            #increase score
            game.score+=100
            game.show_status()
            
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    #allies
    for ally in allies:
        ally.move()

        #Check for collision with ally
        if player.is_collision(ally):
            x=random.randint(-450,450)
            y=random.randint(-450,450)
            ally.goto(x,y)
            game.score -= 50
            game.show_status()

        #Check for missile hit ally
        if missile.is_collision(ally):
            x=random.randint(-450,450)
            y=random.randint(-450,450)
            ally.goto(x,y)
            missile.status = "ready"
            #decrease the score
            game.score -= 50
            game.show_status()

    for particle in particles:
        particle.move()

    

    

