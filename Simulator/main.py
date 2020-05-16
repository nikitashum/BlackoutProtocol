import pygame
import random
import socket

# socket settings
TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024

# pygame initializer
pygame.init()

# global variables
display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)

red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

block_color = (53, 115, 255)

car_width = 73

currentSpeed = 0
thing_speed = 0

currentDanger = 0

firstSend = True

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Demo')
clock = pygame.time.Clock()
carImg = pygame.image.load('Simulator/racecar.png')
pause = False

# try to connect to system over TCP socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("Transmitting on: " + TCP_IP + ":" + str(TCP_PORT))
except Exception as e:
    print(e)


# method for encoding result to bytes and sending it over socket if value has changed or its a first sending
def sendSpeed(speed):
    global currentSpeed
    global firstSend
    valueChanged = currentSpeed != speed
    if valueChanged or firstSend:
        currentSpeed = speed
        speedInBytes = str(speed).encode('utf-8')
        try:
            firstSend = False
            s.send(speedInBytes)
        except Exception as z:
            print(z)
    else:
        return


# increase speed of the car by i
def speedIncreas(i):
    global thing_speed
    if thing_speed < 10:
        thing_speed = thing_speed + i


# decrease speed of the car by i
def speedDecreas(i):
    global thing_speed
    if thing_speed > 0:
        thing_speed = thing_speed - i


# simple decision making data = danger level received from system
def processData(data):
    global currentDanger
    currentDanger = data
    if data > 4:
        speedDecreas(1)
    elif data > 6:
        speedDecreas(2)
    elif data > 7:
        speedDecreas(3)
    else:
        return


# method to draw blue rectangles to display movement
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


# method to update display for speed and danger level
def updateText():
    global currentDanger
    global currentSpeed
    font = pygame.font.SysFont("Arial", 25)
    speed = font.render("Speed: " + str(currentSpeed), True, black)
    danger = font.render("Danger level: " + str(currentDanger), True, black)
    gameDisplay.blit(speed, (0, 0))
    gameDisplay.blit(danger, (0, 20))


# method to display car
def car(x, y):
    gameDisplay.blit(carImg, (x, y))


# method to draw text on the buttons
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                pygame.quit()
                quit()


# method to display buttons
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pygame.font.SysFont("arial", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


# method for quiting the simulator
def quitgame():
    s.close()
    pygame.quit()
    quit()


# method to unpause simulator
def unpause():
    global pause
    pause = False


# method to pause simulator
def paused():
    largeText = pygame.font.SysFont("arial", 115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                pygame.quit()
                quit()

        button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


# method for creating main menu of the simulator
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("Arial", 115)
        TextSurf, TextRect = text_objects("Demo", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Start", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        clock.tick(15)


# main loop of the simulator
def game_loop():
    # scrren size variables
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    # obstacle variables
    thing_startx = 0
    thing_starty = -100
    thing_width = display_width
    thing_height = 20

    gameExit = False

    while not gameExit:
        global thing_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    global pause
                    pause = True
                    paused()
                if event.key == pygame.K_DOWN:
                    speedDecreas(1)
                if event.key == pygame.K_UP:
                    speedIncreas(1)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)
        # create and move obstacle
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        # create and update car position
        car(x, y)
        # update text displaying speed and danger level
        updateText()
        # update display
        pygame.display.update()
        # send current speed
        sendSpeed(thing_speed)
        # receive danger level from system
        try:
            data = s.recv(1024)
            data = data.decode('utf-8')
            data = round(float(data))
            processData(data)
        except Exception as i:
            continue
        clock.tick(30)


# starts simulator
game_intro()
