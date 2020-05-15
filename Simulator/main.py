import pygame
import random
import socket

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024

pygame.init()

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

firstSend = True

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Demo')
clock = pygame.time.Clock()
carImg = pygame.image.load('Simulator/racecar.png')
pause = False

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    print("Transmitting on: " + TCP_IP + ":" + str(TCP_PORT))
except Exception as e:
    print(e)


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


def speedIncreas(i):
    global thing_speed
    if thing_speed < 10:
        thing_speed = thing_speed + i


def speedDecreas(i):
    global thing_speed
    if thing_speed > 0:
        thing_speed = thing_speed - i


def processData(data):
    if data > 4:
        speedDecreas(1)
    elif data > 6:
        speedDecreas(2)
    elif data > 7:
        speedDecreas(3)
    else:
        return


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def currentSpeedText(count):
    font = pygame.font.SysFont("Arial", 25)
    text = font.render("Speed: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.close()
                pygame.quit()
                quit()


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


def quitgame():
    s.close()
    pygame.quit()
    quit()


def unpause():
    global pause
    pause = False


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


def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    thing_startx = random.randrange(0, display_width)
    thing_starty = -100
    thing_width = 20
    thing_height = 20

    gameExit = False

    while not gameExit:
        global thing_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

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

        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        thing_starty += thing_speed
        car(x, y)
        currentSpeedText(thing_speed)

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)

        pygame.display.update()
        # send current speed
        sendSpeed(thing_speed)
        # receive command from system
        try:
            data = s.recv(1024)
            data = data.decode('utf-8')
            data = float(data)
            data = round(data)
            print(data)
            processData(data)
        except Exception as i:
            continue
        clock.tick(60)


game_intro()
