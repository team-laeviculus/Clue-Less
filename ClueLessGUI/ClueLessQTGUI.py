"""
Use this file to manipulate generated files so we don't overwrite anything
"""

from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QColorDialog

from PyQt5.QtCore import QSize
from ClueLessGUI.ClueLess_QTGameboard import Ui_ClueGameBoard
from ClueLessGUI.QTlogin_window import Ui_ClueLoginWindow
from ClueLessGUI.ClientNetworking import ClientNetworking
from Networking.ServerData import GameState
import json
import traceback
import time
import sys
from collections import OrderedDict

app = None  # Main Qt context

nearby_elements = ["roomLounge", "roomConservatory"]

name_conversion = {
    "study_hall": "hall1_2",
    "hall_lounge": "hall1_4",
    "library_billard room": "hall3_2",
    "billard room_dinning room": "hall3_4",
    "conservatory_ballroom": "hall5_2",
    "ballroom_kitchen": "hall5_4",
    "study_library": "hall2_1",
    "hall_billard room": "hall2_3",
    "lounge_dining room": "hall2_5",
    "library_conservatory": "hall4_1",
    "billard room_ballroom": "hall4_3",
    "dining room_kitchen": "hall4_5",
    "Kitchen": "roomKitchen",
    "Conservatory": "roomConservatory",
    "Dining Room": "roomDiningRoom",
    "Ballroom": "roomBallroom",
    "Study": "roomStudy",
    "Hall": "roomHall",
    "Lounge": "roomLounge",
    "Library": "roomLibrary",
    "Billard Room": "roomBilliardRoom"
}


class GameWindow(QtGui.QWindow):
    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        print("Creating GameWindow")


# For updating game status text
class StatusMessageType:
    Good = "green"
    Normal = "black"
    Warning = "yellow"
    Error = "red"


class Notebook:
    # Class for managing checkboxes on notebook stuff
    def __init__(self, parent_widget):
        self.notebook_widget = parent_widget
        self.check_box_widgets = parent_widget.findChildren(QtWidgets.QCheckBox)
        print(f"Check boxes: {len(self.check_box_widgets)}. half: {len(self.check_box_widgets) / 2}")
        self.left_checkboxes = self.check_box_widgets[0:21]

        self.right_checkboxes = self.check_box_widgets[21:]
        self.right_checkboxes_tokens = self.right_checkboxes[0:5]
        self.right_checkboxes_weapons = self.right_checkboxes[5:11]
        self.right_checkboxes_rooms = self.right_checkboxes[11:]

        self.check_boxes = OrderedDict()
        # Initial setup for all check boxes
        for i in range(len(self.check_box_widgets) // 2):
            self.left_checkboxes[i].setEnabled(False)
            # self.left_checkboxes[i].setTriState(False)
            self.right_checkboxes[i].hide()  # Hides all right checkboxes on
            # self.right_checkboxes[i].setTriState(False)
            self.check_boxes[self.check_box_widgets[i].text()] = (self.left_checkboxes[i], self.right_checkboxes[i])

    def show_right_checkboxes(self, current_room):
        for i in self.right_checkboxes_tokens:
            # i.setCheckState(False)
            i.show()
        # for i in self.right_checkboxes_weapons:
        #     # i.setCheckState(False)
        #     i.show()
        # if current_room in self.check_boxes:
        #     room_box = self.check_boxes[current_room]
        #     room_box[1].show()
        #     room_box[1].setCheckState(True)

    def get_checkbox_pair_by_name(self, name):
        """
        Get the pair of checkboxes by name
        :param name: The widget text name
        :return: (left checkbox, right checkbox)
        """
        if name in self.check_boxes:
            return self.check_boxes[name]
        print(f"Error: {name} not found in checkboxes")
        return None

    def get_checkbox_pair_by_index(self, idx):
        """
        Gets a checkbox pair by their integer index
        :param idx: a number, 0-20
        :return: (left checkbox, right checkbox)
        """
        if idx > 0 and idx <= 20:
            return (self.left_checkboxes[idx], self.right_checkboxes[idx])
        print(f"Error {idx} is not within the range of checkbox indices (0-20)")
        return None


class Card:
    MIN_WIDTH = 250

    def __init__(self, name, type):
        self.name = name
        self.type = type


class Room:
    name = None
    positionXsmall = None
    positionXlarge = None
    positionYsmall = None
    positionYlarge = None
    styleSheet = None

    def __init__(self, room_name, room_position_x_small, room_position_x_large, room_position_y_small,
                 room_position_y_large, styleSheet):
        self.name = room_name
        self.positionXsmall = room_position_x_small
        self.positionXlarge = room_position_x_large
        self.positionYsmall = room_position_y_small
        self.positionYlarge = room_position_y_large
        self.styleSheet = styleSheet


class Hall:
    name = None
    positionXsmall = None
    positionXlarge = None
    positionYsmall = None
    positionYlarge = None
    styleSheet = None

    def __init__(self, hall_name, hall_position_x_small, hall_position_x_large, hall_position_y_small,
                 hall_position_y_large, styleSheet):
        self.name = hall_name
        self.positionXsmall = hall_position_x_small
        self.positionXlarge = hall_position_x_large
        self.positionYsmall = hall_position_y_small
        self.positionYlarge = hall_position_y_large
        self.styleSheet = styleSheet


class Player:
    name = None
    token = None
    positionX = None
    positionY = None

    def __init__(self, player_name, token, player_position_x, player_position_y):
        self.name = player_name
        self.token = token
        self.positionX = player_position_x
        self.positionY = player_position_y

    def set_player_position(self, player_position_x, player_position_y):
        self.positionX = player_position_x
        self.positionY = player_position_y


gameboard_Elements = []
Hall1_2 = Hall("hall1_2", 170, 280, 20, 120, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall1_2)
Hall1_4 = Hall("hall1_4", 470, 580, 20, 120, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall1_4)
Hall2_1 = Hall("hall2_1", 10, 120, 150, 250, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall2_1)
Hall2_3 = Hall("hall2_3", 320, 430, 150, 250, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall2_3)
Hall2_5 = Hall("hall2_5", 630, 740, 150, 250, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall2_5)
Hall3_2 = Hall("hall3_2", 170, 280, 280, 380, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall3_2)
Hall3_4 = Hall("hall3_4", 470, 580, 280, 380, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall3_4)
Hall4_1 = Hall("hall4_1", 10, 120, 410, 510, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall4_1)
Hall4_3 = Hall("hall4_3", 320, 430, 410, 510, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall4_3)
Hall4_5 = Hall("hall4_5", 630, 740, 410, 510, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall4_5)
Hall5_2 = Hall("hall5_2", 170, 280, 520, 640, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall5_2)
Hall5_4 = Hall("hall5_4", 470, 580, 520, 640, "background-color: rgb(125, 125, 125);")
gameboard_Elements.append(Hall5_4)
Study = Room("roomStudy", 10, 120, 20, 120,
             "background-color: rgb(170, 170, 127);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Study)
Hall = Room("roomHall", 320, 430, 20, 120,
            "background-color: rgb(85, 255, 255);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Hall)
Lounge = Room("roomLounge", 630, 740, 20, 120,
              "background-color: rgb(255, 170, 0);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Lounge)
Library = Room("roomLibrary", 10, 120, 280, 380,
               "background-color: rgb(170, 85, 127);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Library)
Billiard_Room = Room("roomBilliardRoom", 320, 430, 280, 380,
                     "background-color: rgb(0, 170, 127);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Billiard_Room)
Dining_Room = Room("roomDiningRoom", 630, 740, 280, 380,
                   "background-color: rgb(255, 255, 127);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Dining_Room)
Conservatory = Room("roomConservatory", 10, 120, 520, 640,
                    "background-color: rgb(170, 170, 255);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Conservatory)
Ballroom = Room("roomBallroom", 320, 430, 520, 640,
                "background-color: rgb(255, 170, 127);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Ballroom)
Kitchen = Room("roomKitchen", 630, 740, 520, 640,
               "background-color: rgb(125, 125, 125);\nborder: 1px solid black;\ncolor: rgb(0, 0, 0);")
gameboard_Elements.append(Kitchen)


class MainWindow(QMainWindow):

    def __init__(self, qtcontext):
        self.app = qtcontext

        QMainWindow.__init__(self)
        self.setMinimumSize(QtCore.QSize(900, 450))
        self.setMaximumSize(QtCore.QSize(1464, 949))
        self.networking = ClientNetworking(self)

        # Move Button Add-On
        self._running = False

        self.setWindowTitle("ClueLess Prototype - Please Login")

        ### LOGIN FORM WIDGET
        self.login_form_widget = QWidget()
        self.clue_login_window = Ui_ClueLoginWindow()
        self.clue_login_window.setupUi(self.login_form_widget)

        ### GameBoard Widget
        self.game_board_widget = QWidget()
        self.game_board_ui = Ui_ClueGameBoard()
        self.game_board_ui.setupUi(self.game_board_widget)

        # Status and message updates
        self.game_status = self.game_board_ui.game_status_window
        self.chat_window = self.game_board_ui.chat_text_display_box
        self.last_chat_message = None

        # Set the widget being displayed to the login form
        self.setCentralWidget(self.login_form_widget)

        self.dialogs = list()
        # Notebook checkboxes
        self.notebook = Notebook(self.game_board_ui.gbNotebook)

        # self.notebook.show_right_checkboxes("Hall")

        print(f"TEST Checkboxes: {self.notebook.get_checkbox_pair_by_index(4)}")
        print(f"Test by name: {self.notebook.get_checkbox_pair_by_name('Rope')}")

        # for i in range(self.notebook.count()):
        #     print(f"Adding checkbox widget: {self.notebook.item(i)}")
        #     self.check_boxes.append(self.notebook.item(i))

        self.my_profile = None  # Contains name, token, location dict
        self.my_cards = None  # Contains cards
        self.game_data_initialized = False  # Boolean for one time initialization calls
        self.players = OrderedDict()

        ######################################
        ########### Button Actions ###########
        ######################################
        # self.quit_game_button.clicked.connect(self.quit_callback)
        # self.send_message_button.clicked.connect(self.send_message_callback)
        # self.make_suggestion_button.clicked.connect(self.make_suggestion_callback)
        # self.make_accusation_button.clicked.connect(self.make_accusation_callback)
        # Create Profile, also accepts enter button
        self.clue_login_window.create_profile_button.clicked.connect(self.login_button_callback)
        self.clue_login_window.username_input_field.returnPressed.connect(
            self.clue_login_window.create_profile_button.click)

        self.game_board_ui.make_move_button.clicked.connect(
            lambda: self.make_move_callback(nearby_array=nearby_elements))
        self.game_board_ui.groupBox.mousePressEvent = self.moveToken

    def moveToken(self, event):
        print("Got a response")
        widgets = (self.game_board_ui.gridLayout.itemAt(i).widget() for i in
                   range(self.game_board_ui.gridLayout.count()))

        x = event.x()
        y = event.y()

        for item in gameboard_Elements:
            if (item.positionXsmall < x < item.positionXlarge) and (item.positionYsmall < y < item.positionYlarge):
                print(item.name)
                for widget in widgets:
                    if (item.name in widget.objectName()) and ("moving" in widget.objectName()):
                        print(item.name)
                        self.game_board_ui.suspectMrsPeacock.move(x, y)
        location = "x: {0},  y: {1}".format(x, y)
        print(location)
        self._running = False

    def create_profile_callback(self, reply):
        """
        ClientNetworking Callback for creating a profile
        :param reply:
        :return:
        """
        print("\nCREATE PROFILE CALLBACK CALLED")
        try:
            data, er = self.networking.reply_to_json(reply)
            status_window = self.clue_login_window.create_profile_server_status_label

            def error_message(msg: str):
                status_window.setStyleSheet("QLabel { font: 9pt; color: red }")
                status_window.setText(msg)

            # Success!!!
            if er == QtNetwork.QNetworkReply.NoError:
                print(f"Data: {data}")
                print(f"Created profile for {data['name']}")
                status_window.clear()
                status_window.setStyleSheet("QLabel { font-weight: bold; color: green }")
                status_window.setText(f"Profile {data['name']} created! Entering game {data['game_id']} in 1s")

                self.app.processEvents()
                self.login_form_widget.hide()
                self.my_profile = data
                self.networking.set_profile_data(self.my_profile)  # Hopefully this is passed by reference

                self.__launch_gameboard(data)

                # Populate the chat window with some initial messages

            elif er == QtNetwork.QNetworkReply.ProtocolInvalidOperationError:
                if data:
                    error_message(f"Error! {data['name']} Already Taken.")
                else:
                    error_message(f"Error! Name already taken")
                    traceback.print_exc()
            elif er == QtNetwork.QNetworkReply.ConnectionRefusedError:
                error_message(f"{reply.errorString()} - {self.networking.base_url}")
            else:
                error_message(f"Unhandled Error:")
                # error_message(f"Unhandled Error: {reply.errorString()}")

        except Exception as e:
            print(f"Exception! {e}")
            traceback.print_exc()

    def status_update_callback(self, reply):
        """
        This gets the game state from the server
        :param reply:
        :return:
        """
        print("\n[Status Update]  CALLBACK CALLED")
        status, err = self.networking.reply_to_json(reply)
        print(f"NEW STATUS [{err}]: {status}")
        if status:
            if status['last_chat_message'] != self.last_chat_message:
                self.add_message_to_chat_window(f"{status['last_chat_message']}")
                self.last_chat_message = status['last_chat_message']

            # Terrible way to do this but whatever
            # new_players = set(status['players'].keys()) - set(self.players.keys())
            for p, profile in status['players'].items():
                if not p in self.players:
                    self.players[p] = status['players'][p]
                    print(f"Added new player: {status['players'][p]}")
                    self.add_message_to_chat_window(f"Player {status['players'][p]['name']} Joined the game")

        # Main game 'loop' in a sense
        if status['state'] == GameState.GAME_RUNNING:
            if not self.game_data_initialized:
                print("Initializing Game State")
                self.init_game_data()

            if 'turn' in status:
                current_players_turn = status['turn']['name']
                if current_players_turn == self.my_profile['name']:
                    self.update_game_status("Its my Turn!!")
                else:
                    # Waiting for turn
                    self.update_game_status(f"Waiting for player {current_players_turn} to finish turn")

    def init_game_data(self):
        # Called only once when the game starts to get needed data from server
        print("\n")
        print("-" * 40)
        print("[init_game_data]: Initializing Game Data")
        if self.game_data_initialized is False:
            print("[init_game_data]: initializing cards")

            self.networking.get_my_cards(self.get_cards_callback)

    def get_cards_callback(self, reply):
        print(f"\nGET CARDS")
        print("-" * 40)
        cards, er = self.networking.reply_to_json(reply)
        print(f"CARDS[{er}]: {cards}")
        # Sets players cards class variable
        if not "error" in cards:
            self.my_cards = cards['cards']
            self.add_message_to_chat_window(f"My Cards: {self.my_cards}")
            self.game_data_initialized = True

    def __launch_gameboard(self, data):
        """
        After player logs in, launches gamebaord player will be using
        :return:
        """
        self.setCentralWidget(self.game_board_widget)
        self.setWindowTitle(f"ClueLess Prototype - Server #{self.networking.game_id}")
        self.game_board_widget.show()
        self.update_game_status("Waiting for players to join...")
        # self.add_message_to_chat_window(f"Player: {data['name']} joined the game!")
        # Start repeated requests for game updates
        print(f"LAUNCHING GAMEBOARD")
        self.networking.set_game_id(data['game_id'])
        self.networking.set_status_callback(self.status_update_callback)
        self.networking.get_server_status()
        self.networking.start_server_status_tick()

    def quit_callback(self):
        print("Exiting ClueGameBoard prototype")
        # Dialog.close()

    def send_message_callback(self):
        print("send message clicked")

    def make_move_callback(self, nearby_array):
        print("Make move button Clicked")
        self.game_board_ui.make_suggestion_button.setDisabled(True)
        widgets = (self.game_board_ui.gridLayout.itemAt(i).widget() for i in
                   range(self.game_board_ui.gridLayout.count()))
        for widget in widgets:
            for i in nearby_array:
                if widget.objectName() == i:
                    new_name = widget.objectName()
                    widget.setObjectName(new_name + "_moving")
                    widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "border: 5px solid yellow;\n"
                                         "color: rgb(0, 0, 0);")
        self._running = True
        while self._running:
            QtGui.QGuiApplication.processEvents()
            time.sleep(0.05)
        print("Still got it")
        widgets_list = (self.game_board_ui.gridLayout.itemAt(i).widget() for i in
                        range(self.game_board_ui.gridLayout.count()))
        for current in widgets_list:
            for i in nearby_array:
                if i in current.objectName():
                    print(current)
                    current.setObjectName(i)
                    for item in gameboard_Elements:
                        if item.name == current.objectName():
                            current.setStyleSheet(item.styleSheet)

        self.game_board_ui.make_suggestion_button.setDisabled(False)

    def make_suggestion_callback(self, nearby_array):
        print("Make Suggestion Clicked")
        widgets = (self.game_board_ui.gridLayout.itemAt(i).widget() for i in
                   range(self.game_board_ui.gridLayout.count()))
        for widget in widgets:
            for i in nearby_array:
                if widget.objectName() == i:
                    new_name = widget.objectName()
                    widget.setObjectName(new_name + "_moving")
                    widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "border: 5px solid yellow;\n"
                                         "color: rgb(0, 0, 0);")
        self.game_board_ui.roomStudy.mousePressEvent = self.doSomething
        # QtGui.QGuiApplication.processEvents()
        # print(self.game_board_ui.roomStudy.objectName())

    def tmp_make_suggestion_callback(self, nearby_array):
        print("Make Suggestion Clicked")
        # From Phillip, get player, weapon, room from user
        game_id = self.networking.game_id
        address_string = "/games/" + game_id + "/turn"
        data_dict = {"name": self.profile_name, "move_type": "accusation",
                     "move_info": {"player": None, "weapon": None, "room": None}}
        self.networking.post_json(address_string, json.dumps(data_dict),
                                  self.get_suggestion_callback)

    def get_suggestion_callback(self, reply):
        """
        ClientNetworking Callback for making a suggestion
        :param reply:
        :return:
        """
        print("\nSUGGESTION CALLBACK CALLED")
        try:
            data, er = self.networking.reply_to_json(reply)
            status_window = self.clue_login_window.create_profile_server_status_label

            def error_message(msg: str):
                status_window.setStyleSheet("QLabel { font: 9pt; color: red }")
                status_window.setText(msg)

            # Success!!!
            if er == QtNetwork.QNetworkReply.NoError:
                print(f"Returned suggestion data")
                print(f"Data: {data}")

                # if no error, no status msg about returned suggestion?
                # TODO: what should this actually do?
                # Call methods here

            elif er == QtNetwork.QNetworkReply.ProtocolInvalidOperationError:
                if data:
                    # error_message(f"Error! {data['name']} Already Taken.")
                    # Would any deliberate error msgs be returned for this?
                    pass
                else:
                    print("Some other error")
                    traceback.print_exc()
            elif er == QtNetwork.QNetworkReply.ConnectionRefusedError:
                error_message(f"{reply.errorString()} - {self.networking.base_url}")
            else:
                error_message(f"Unhandled Error: {reply.errorString()}")

        except Exception as e:
            print(f"Exception! {e}")
            traceback.print_exc()

    def make_accusation_callback(self):
        print("Make Accusation Clicked")

    def login_callback(self):
        print("Login called")
        print(f"TEXT entered: {self.clue_login_window.username_input_field.text()}")

    def login_button_callback(self):
        """
        login button click (or enter key press) callback. Calls ClientNetworking to register
        another callback function.
        :return:
        """
        self.profile_name = self.clue_login_window.username_input_field.text()
        status_label = self.clue_login_window.create_profile_server_status_label
        status_label.setStyleSheet("QLabel { color: yellow }")
        status_label.setText("Connecting to server...")

        print(f"[login screen] Profile name entered: {self.profile_name}")
        self.networking.post_json("/games/players", json.dumps({"name": self.profile_name}),
                                  self.create_profile_callback)

    def update_game_status(self, msg: str, message_type: StatusMessageType = StatusMessageType.Normal):
        print(f"Game Status updated: {msg}")
        self.game_status.setStyleSheet("QLabel { color: white }")
        self.game_status.setText(msg)

    def add_message_to_chat_window(self, msg: str, type: str = "N"):
        print(f"New game chat status {msg}")
        self.chat_window.setText(self.chat_window.text() + f"\n[{type}]: {msg}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec_())
