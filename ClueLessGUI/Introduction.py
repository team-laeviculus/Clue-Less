import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)


card_rooms = ['conservatory.png', 'hall.png']
card_weapons = ['knife.png', 'poison.png']
card_characters = ['Scarlet.png', 'Mustard.png']
current_character = 0
current_room = 0
current_weapon = 0


gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('CLUE-LESS')
clock = pygame.time.Clock()

Logo = pygame.image.load('sherlock-holmes.jpg')
background = pygame.image.load('background.png')

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def card_shuffle(x,y,w,h,card_list):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)

    global current_room
    global current_character
    global current_weapon

    if card_list == card_rooms:
        card_loop = card_list[current_room]
        current_card = pygame.image.load(card_loop)
        gameDisplay.blit(current_card, (x, y))

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1:
                if current_room < card_list.index(card_list[-1]):
                    current_room += 1
                else:
                    current_room = 0

    elif card_list == card_weapons:
        card_loop = card_list[current_weapon]
        current_card = pygame.image.load(card_loop)
        gameDisplay.blit(current_card, (x, y))

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1:
                if current_weapon < card_list.index(card_list[-1]):
                    current_weapon += 1
                else:
                    current_weapon = 0

    else:
        card_loop = card_list[current_character]
        current_card = pygame.image.load(card_loop)
        gameDisplay.blit(current_card, (x, y))

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1:
                if current_character < card_list.index(card_list[-1]):
                    current_character += 1
                else:
                    current_character = 0

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def leave():
    pygame.quit()
    quit()

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("CLUE-LESS", largeText)
        TextRect.center = ((display_width / 2), 75)
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(Logo, (300, 125))

        button("START", 100, 450, 150, 50, green, bright_green, game_loop)
        button("EXIT", 500, 450, 150, 50, red, bright_red, leave)
        pygame.display.update()
        clock.tick(15)


def game_loop():

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)
        gameDisplay.blit(background, (0, 0))

        card_shuffle(620, 10, 152, 103, card_rooms)
        card_shuffle(620, 120, 152, 103, card_characters)
        card_shuffle(620, 231, 152, 103, card_weapons)
        button("QUIT", 625, 525, 150, 50, green, bright_green, game_intro)
        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
pygame.quit()
quit()