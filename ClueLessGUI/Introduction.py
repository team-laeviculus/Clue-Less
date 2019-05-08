import pygame
import pygame_textinput
import thorpy
import time
import random

pygame.init()

display_width = 1000
display_height = 700

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

def button(msg,butt,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",butt)
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

def my_alert_1():
    thorpy.launch_nonblocking_alert(title="This is a non-blocking alert!",
                                text="This is the text..",
                                ok_text="Ok, I've read",
                                font_size=12,
                                font_color=(255,0,0))
    print("Proof that it is non-blocking : this sentence is printing at exit!")

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def leave():
    pygame.quit()
    quit()

def move():
    pass

def make_suggestion():
    pass

def make_accusation():
    pass

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
        TextRect.center = ((display_width / 2), (75))
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(Logo, (300, 125))

        button("START", 20, 100, 450, 100, 50, green, bright_green, game_loop)
        button("JOIN", 20, 300, 450, 100, 50, green, bright_green, game_join)
        button("EXIT", 20, 500, 450, 100, 50, red, bright_red, leave)

        pygame.display.update()
        clock.tick(15)


def game_join():
    join = True

    name = ""

    textInput = pygame_textinput.TextInput( text_color=white,
                                           cursor_color=white)
    while join:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)

        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Enter Name:", largeText)
        TextRect.center = ((display_width / 2), ((display_height / 2)-50))
        gameDisplay.blit(TextSurf, TextRect)

        events = pygame.event.get()
        # Feed it with events every frame
        if textInput.update(events) == True:
            name=textInput.get_text()
        # Blit its surface onto the screen
        gameDisplay.blit(textInput.get_surface(), (((display_width/2)-100), display_height/2))

        button("BACK", 20, 625, 525, 150, 50, red, bright_red, game_intro)
        button("START", 20, 25, 525, 150, 50, green, bright_green, game_wait)

        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects(name, largeText)
        TextRect.center = ((display_width / 2), ((display_height / 2)+150))
        gameDisplay.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(120)


def game_wait():
    wait = True

    while wait:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(black)

        largeText = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects("Waiting on game...", largeText)
        TextRect.center = ((display_width / 2), ((display_height / 2) - 50))
        gameDisplay.blit(TextSurf, TextRect)

        button("BACK", 20, 625, 525, 150, 50, red, bright_red, game_intro)

        pygame.display.update()
        clock.tick(15)


def game_loop():

    gameExit = False

    while not gameExit:

        # black background and image
        gameDisplay.fill(black)
        gameDisplay.blit(background, (200, 75))

        #Notebook Checkbox
        checker_one = thorpy.Checker("Colonel Mustard")
        checker_two = thorpy.Checker("Professor Plum")
        checker_three = thorpy.Checker("Mr.Green")
        checker_four = thorpy.Checker("Ms.Peacock")
        checker_five = thorpy.Checker("Ms.Scarlet")
        checker_six = thorpy.Checker("Ms.White")
        checker_seven = thorpy.Checker("Knife")
        checker_eight = thorpy.Checker("Candlestick")
        checker_nine = thorpy.Checker("Revolver")
        checker_ten = thorpy.Checker("Rope")
        checker_eleven = thorpy.Checker("Lead Pipe")
        checker_twelve = thorpy.Checker("Wrench")
        checker_thirteen = thorpy.Checker("Hall")
        checker_fourteen = thorpy.Checker("Lounge")
        checker_fifteen = thorpy.Checker("Dining Room")
        checker_sixteen = thorpy.Checker("Kitchen")
        checker_seventeen = thorpy.Checker("Ballroom")
        checker_eighteen = thorpy.Checker("Conservatory")
        checker_nineteen = thorpy.Checker("Billiard Room")
        checker_twenty = thorpy.Checker("Library")
        checker_twentyone = thorpy.Checker("Study")
        notebook_elements = [checker_one, checker_two, checker_three, checker_four, checker_five, checker_six, checker_seven, checker_eight,
                    checker_nine, checker_ten, checker_eleven, checker_twelve, checker_thirteen, checker_fourteen, checker_fifteen, checker_sixteen,
                    checker_seventeen, checker_eighteen, checker_nineteen, checker_twenty, checker_twentyone]
        notebook_box = thorpy.Box(elements=notebook_elements)
        notebook_box.fit_children(margins=(10, 10))
        notebook_box.set_main_color((220, 220, 220, 180))
        notebook_menu = thorpy.Menu(notebook_box)
        for element in notebook_menu.get_population():
            element.surface = gameDisplay
        notebook_box.set_topleft((825, 20))
        notebook_box.blit()
        notebook_box.update()

        #Game Status Text Box
        game_status_text = "Game Status Text ..."
        game_status = thorpy.OneLineText(text=game_status_text)
        game_status_elements = [game_status]

        game_status_box = thorpy.Box(elements=game_status_elements)
        game_status_box.fit_children(margins=(10, 10))
        game_status_box.set_main_color((220, 220, 220, 180))
        game_status_menu = thorpy.Menu(game_status_box)
        for element in game_status_menu.get_population():
            element.surface = gameDisplay
        game_status_box.set_topleft((200, 20))
        game_status_box.blit()
        game_status_box.update()

        #Chat Window
        chat_message = "Sample Chat Message\n Additional Message"
        chat_window = thorpy.MultilineText(text=chat_message, size=(200, 825))
        inserter = thorpy.Inserter(name="Inserter: ", value="Write here.")
        chat_message_elements = [chat_window, inserter]

        chat_window_box = thorpy.Box(elements=chat_message_elements)
        chat_window_box.fit_children(margins=(10, 10))
        chat_window_box.set_main_color((220, 220, 220, 180))
        chat_window_menu = thorpy.Menu(chat_window_box)
        for element in chat_window_menu.get_population():
            element.surface = gameDisplay
        chat_window_box.set_topleft((20, 200))
        chat_window_box.blit()
        chat_window_box.update()


        #card_shuffle(620, 10, 152, 103, card_rooms)
        card_shuffle(50, 20, 152, 103, card_characters)
        #card_shuffle(620, 231, 152, 103, card_weapons)

        button("Move", 20, 825, 490, 150, 40, red, bright_red, move)
        button("Make Suggestion", 15, 825, 540, 150, 40, red, bright_red, make_suggestion)
        button("Make Accusation", 15, 825, 590, 150, 40, red, bright_red, make_accusation)
        button("QUIT", 20, 825, 650, 150, 40, red, bright_red, game_intro)

        for event in pygame.event.get():
            notebook_menu.react(event)
            game_status_menu.react(event)
            #add other menus
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(120)


game_intro()
game_loop()
pygame.quit()
quit()