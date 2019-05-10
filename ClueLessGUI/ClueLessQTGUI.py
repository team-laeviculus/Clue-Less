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
        self.clue_login_window.create_profile_button.clicked.connect(self.start_clue_gui)
        self.clue_login_window.username_input_field.returnPressed.connect(
            self.clue_login_window.create_profile_button.click)



    def create_profile_callback(self, reply):
        # print(f"Error code: {reply.error}")
        try:
            data, er = ClientNetworking.reply_to_json(reply)
            status_window = self.clue_login_window.create_profile_server_status_label

            # Success!!!
            if er == QtNetwork.QNetworkReply.NoError:
                print(f"Created profile for {data['name']}")
                status_window.clear()
                status_window.setStyleSheet("QLabel { font-weight: bold; color: green }")
                status_window.setText(f"Profile {data['name']} created! Entering game in 3s")
                app.processEvents()
                time.sleep(3)

                self.login_form_widget.hide()
                self.setCentralWidget(self.game_board_widget)
                self.game_board_widget.show()


            elif er == QtNetwork.QNetworkReply.ProtocolInvalidOperationError:
                print(f"Name Taken!!!")
                status_window.setStyleSheet("QLabel { font-weight: bold; color: red }")
                status_window.setText(f"Error! Name Already Taken.")

            else:
                print(f"Other Error: {er}")

        except Exception as e:
            print(f"ExceptioN: {e}")
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

    def start_clue_gui(self):
        """
        launches main game
        :return:
        """
        requested_profile_name = self.clue_login_window.username_input_field.text()
        print(f"TEXT entered: {requested_profile_name}")
        try:
            self.networking.post_json("/games/players", json.dumps({"name": requested_profile_name}), self.create_profile_callback)
        except Exception as e:
            print(f"ERROR {e}")
            traceback.print_exc()


        # self.login_form_widget.hide()
        # self.setCentralWidget(self.game_board_widget)
        # self.game_board_widget.show()

app = QtWidgets.QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())