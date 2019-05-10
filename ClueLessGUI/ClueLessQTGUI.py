"""
Use this file to manipulate generated files so we don't overwrite anything
"""

from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from PyQt5.QtCore import QSize
from ClueLessGUI.ClueLess_QTGameboard import Ui_ClueGameBoard
from ClueLessGUI.QTlogin_window import Ui_ClueLoginWindow
from ClueLessGUI.ClientNetworking import ClientNetworking
import json
import traceback
import time
import sys

class GameWindow(QtGui.QWindow):
    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)
        print("Creating GameWindow")


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QtCore.QSize(1464, 949))
        self.setMaximumSize(QtCore.QSize(1464, 949))
        self.networking = ClientNetworking(self)

        self.setWindowTitle("ClueLess Prototype - Please Login")

        ### LOGIN FORM WIDGET
        self.login_form_widget = QWidget()
        self.clue_login_window = Ui_ClueLoginWindow()
        self.clue_login_window.setupUi(self.login_form_widget)

        ### GameBoard Widget
        self.game_board_widget = QWidget()
        self.game_board_ui = Ui_ClueGameBoard()
        self.game_board_ui.setupUi(self.game_board_widget)

        self.game_status = self.game_board_ui.game_status_window
        self.chat_window = self.game_board_ui.chat_text_display_box

        # Set the widget being displayed to the login form
        self.setCentralWidget(self.login_form_widget)

        self.dialogs = list()
        #
        # app = QtWidgets.QApplication(sys.argv)
        # Form = QtWidgets.QWidget()
        # ui = Ui_ClueLoginWindow()
        # ui.setupUi(Form)
        # Form.show()
        # sys.exit(app.exec_())


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



    def create_profile_callback(self, reply):
        """
        ClientNetworking Callback for creating a profile
        :param reply:
        :return:
        """
        try:
            data, er = ClientNetworking.reply_to_json(reply)
            status_window = self.clue_login_window.create_profile_server_status_label

            def error_message(msg: str):
                status_window.setStyleSheet("QLabel { font: 9pt; color: red }")
                status_window.setText(msg)
            # Success!!!
            if er == QtNetwork.QNetworkReply.NoError:
                print(f"Created profile for {data['name']}")
                status_window.clear()
                status_window.setStyleSheet("QLabel { font-weight: bold; color: green }")
                status_window.setText(f"Profile {data['name']} created! Entering game {data['game_id']} in 1s")
                app.processEvents()
                time.sleep(1)

                self.login_form_widget.hide()
                self.setCentralWidget(self.game_board_widget)
                self.game_board_widget.show()
                self.update_game_status("Waiting for players to join...")
                self.add_message_to_chat_window(f"Player: {data['name']} joined the game!")
                # Start repeated requests for game updates
                self.networking.set_game_id(data['game_id'])
                self.networking.start_server_status_tick()


                # Populate the chat window with some initial messages

            elif er == QtNetwork.QNetworkReply.ProtocolInvalidOperationError:
                error_message(f"Error! {data['name']} Already Taken.")

            elif er == QtNetwork.QNetworkReply.ConnectionRefusedError:
                error_message(f"{reply.errorString()} - {self.networking.base_url}")
            else:
                error_message(f"Unhandled Error: {reply.errorString()}")

        except Exception as e:
            print(f"Exception! {e}")
            traceback.print_exc()


    def quit_callback(self):
        print("Exiting ClueGameBoard prototype")
        # Dialog.close()

    def send_message_callback(self):
        print("send message clicked")

    def make_suggestion_callback(self):
        print("Make Suggestion Clicked")

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

        print(f"Profile name entered: {self.profile_name}")
        self.networking.post_json("/games/players", json.dumps({"name": self.profile_name}), self.create_profile_callback)


    def update_game_status(self, msg: str):
        print(f"Game Status updated: {msg}")
        self.game_status.setText(msg)

    def add_message_to_chat_window(self, msg: str):
        print(f"New game chat status {msg}")
        self.chat_window.setText(self.chat_window.text() + f"\n{msg}")

# Main application window context
app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())