# This is just a placeholder for the time being

import pygame
import time
import queue
import json


class AbstractGUI(object):

    window_height = 0
    window_width = 0
    window_caption = ""
    window_initialized = False
    window_ptr = None
    latest_message = None
    event_loop_running = True
    clock = None

    BACKGROUND_COLOR = (255, 255, 255)  # White RGB value
    # TODO: Add actual logger
    log = lambda msg: print(f"[GUI LOGGER]: {msg}")

    def __init__(self, height, width, caption="Default Caption", msg_queue=None):
        # Basic Constructor
        self.window_height = height
        self.window_width = width
        self.window_caption = caption
        self.msg_queue = msg_queue
        self.run_once = False # TODO REMOVE


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



                # Iterate through events registered in the event loop
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.event_loop_running = False
                        # Exits the window

                self.window_ptr.fill(self.BACKGROUND_COLOR)

                if self.msg_queue and not self.msg_queue.empty():
                    self.latest_message = self.msg_queue.get()
                    self.run_once = False
                    print("New Message Queue Item!")
                    print(f"{self.latest_message['client']}")
                    print(f"{self.latest_message['server']}")
                    print("\n\r")
                self.display_latest_messages()

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
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    def render_message(self, text, font_size, x_offset=0.0, y_offset=0.0):
        try:
            largeTextMessage = pygame.font.Font('freesansbold.ttf', font_size)
            TextSurface, TextRectangle = self.text_objects(text, largeTextMessage)
            TextRectangle.center = ((self.window_width / 2) + x_offset, (self.window_height / 2) + y_offset)
            self.window_ptr.blit(TextSurface, TextRectangle)
        except Exception as e:
            print(f"Error!: {e}")

    def hello_world_message(self):
        self.render_message("Hello World from game window!", 32)

    def display_latest_messages(self):
        if self.latest_message is None:
            self.hello_world_message()
        else:
            self.render_message(self.latest_message['client'], 12, x_offset=-40)
            server_messages = self.latest_message['server'][0]
            json_server_msg = self.latest_message['server'][1]
            y_off = 20
            if not type(json_server_msg) is list:
                json_server_msg = [json_server_msg]
            # We have to re-draw the messages every tick
            for item in json_server_msg:
                self.render_message(server_messages + json.dumps(item), 12, x_offset=-40, y_offset=y_off)
                y_off += 20


def thread_method(msg_queue=None):
    window = AbstractGUI(600, 800, "Test Window", msg_queue)
    window.initializeWindow()
    window.startEventLoop()


# for testing purposes

if __name__ == "__main__":
    print("Starting window test!")
    TestWindow = AbstractGUI(600, 800, "Hello World!")
    TestWindow.initializeWindow()
    TestWindow.startEventLoop()
