# David Ding
# Cool visualization of mapping points, etc
# May 6th 2018

# Imports
import pygame
import random
import math
from win32api import GetSystemMetrics


# Classes
# point is a class for the actual points that are moving through the space
class point():
    def __init__(self, x, y):
        # x_position, y_position are pretty self-explanatory
        # pos refers to the tuple variable that x, y are stored under
        # opacity controls how the animation fades to black
        # color is the color
        # radius is the size of the "node" that is being placed
        # angle controls the direction that each point travels in
        self.x_position = x
        self.y_position = y
        self.pos = (self.x_position, self.y_position)
        self.opacity = random.randint(0, 100)
        self.color = (255 - self.opacity, 255 - self.opacity, 255 - self.opacity)
        self.radius = 3
        self.angle = random.randint(0, 360)

    # update, called every frame
    def update(self):
        self.x_position += 2*math.cos(self.angle)
        self.y_position += 2*math.sin(self.angle)
        self.color = (255 - self.opacity, 255 - self.opacity, 255 - self.opacity)
        self.pos = (self.x_position, self.y_position)
        self.opacity += 1


# this happens on click, creates a certain amount of new points
def clicked(x, y):
    # arr is a temporary array to store the classes
    arr = []
    for i in range(random.randint(3, 6)):
        arr.append(point(x, y))
    return arr


# gets position of mouse
def get_mouse():
    # mx, my are x, y coordinates of the point
    # mb, mr are booleans that record mouse button and mouse (right) button
    mx, my = pygame.mouse.get_pos()
    mb, mr = pygame.mouse.get_pressed()[0], pygame.mouse.get_pressed()[1]
    return mx, my, mb, mr


# distance calculator between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((math.pow((x2-x1), 2)) + math.pow((y2-y1), 2))


# MAIN
# running stores the state of the animation
# SCREEN_SIZE stores how big the screen is, usually taken by win32api's system metrics
# screen is the screen in which everything will be displayed
# dots stores all the points
# myClock stores game ticks
# alreadyclicked stores whether or not the mouse is already down or not, to prevent press-hold bugs
pygame.init()
running = True
SCREEN_SIZE = (GetSystemMetrics(0), GetSystemMetrics(1))
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
dots = []
myClock = pygame.time.Clock()
alreadyclicked = False

# main loop
while running:
    # quit event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.K_ESCAPE:
            running = False
    # another quit event listener
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    # gets mouse
    mx, my, mb, mr = get_mouse()

    # random point spawning
    randrand = random.randint(0, 100)
    if randrand >= 88:
        dots.append(point(random.randint(80, 1600), random.randint(0, 1020)))

    # press-hold mouse toggle
    if mb == 0:
        alreadyclicked = False

    if not alreadyclicked:
        if mb == 1:
            dots += clicked(mx, my)
            alreadyclicked = True

    # updates to refresh screen
    screen.fill((0, 0, 0))

    # cycles through every vertex in the array and displays it onto the screen
    for vertex in dots:
        vertex.update()
        pygame.draw.circle(screen, vertex.color, (int(vertex.x_position), int(vertex.y_position)), vertex.radius, 0)
        # check if the vertex has already faded to black (invisible), in which case remove it from the array to be
        # iterated through
        if vertex.opacity >= 255:
            dots.remove(vertex)

    # draws the lines connecting two dots together, forming a connected graph. However, I found that this looked
    # better when the furthest distance was changed so it was limited to 250 pixels in length
    for i in range(len(dots)):
        for j in range(len(dots) - 1):
            if distance(dots[i].x_position, dots[i].y_position, dots[j].x_position, dots[j].y_position) <= 250:
                pygame.draw.line(screen, dots[i].color, dots[i].pos, dots[j].pos, 1)

    # update!!!
    myClock.tick(60)
    pygame.display.flip()

# Wow Mr. Ching, my program actually quits pygame for once. Can you believe it?
pygame.quit()

