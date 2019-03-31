# This is just a placeholder for the time being

import pygame
import time

class AbstractGUI(object):

    window_height = 0
    window_width = 0
    window_caption = ""
    window_initialized = False
    window_ptr = None

    event_loop_running = True
    clock = None

    BACKGROUND_COLOR = (255,255,255) # White RGB value
    # TODO: Add actual logger
    log = lambda msg: print(f"[GUI LOGGER]: {msg}")

    def __init__(self, height, width, caption="Defaul Caption"):
        # Basic Constructor
        self.window_height = height
        self.window_width = width
        self.window_caption = caption

        print(f"Window Constructed: height = {height}, width = {width}, caption = {caption}")


    def initializeWindow(self):
        # Sets up some of the initial values pygame requires
        self.window_ptr = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(self.window_caption)
        self.clock = pygame.time.Clock()
        self.window_initialized = True
        pygame.init()

    def startEventLoop(self, tick_rate=60):
        # Main GUI event loop. This is where all events get parsed (input), and
        # any type of graphical element gets registered to be rendered. ORDER IS IMPORTANT!
        # tick_rate = time to sleep between loops, in ms
        if self.window_initialized:

            while self.event_loop_running:

                # Iterate throught events registered in the event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.event_loop_running = False
                        #Exits the window

                self.window_ptr.fill(self.BACKGROUND_COLOR)
                self.hello_world_message()

                # Redraw
                pygame.display.update()
                # Time duration between next loop update. Used to reduce CPU usage
                self.clock.tick(tick_rate)



            # On event loop exit:
            pygame.quit()
            #quit()
        else:
            self.log("Error! Can't start event loop unless window has been initialized")

    # Example of rendering text, no coordinates included so text is just in center of screen
    def text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def render_message(self, text, font_size):
        try:
            largeTextMessage = pygame.font.Font('freesansbold.ttf', font_size)
            TextSurface, TextRectangle = self.text_objects(text, largeTextMessage)
            TextRectangle.center = ((self.window_width / 2), (self.window_height / 2))
            self.window_ptr.blit(TextSurface, TextRectangle)
        except Exception as e:
            print(f"Error!: {e}")
        pygame.display.update()
        #time.sleep(2)
        #self.startEventLoop()

    def hello_world_message(self):
        self.render_message("Hello World from game window!", 32)



def thread_method():
    window = AbstractGUI(600, 800, "Test Window")
    window.initializeWindow()
    window.startEventLoop()


# for testing purposes

if __name__ == "__main__":
    print("Starting window test!")
    TestWindow = AbstractGUI(600, 800, "Hello World!")
    TestWindow.initializeWindow()
    TestWindow.startEventLoop()
