"""
Use this file to manipulate generated files so we don't overwrite anything
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from PyQt5.QtCore import QSize
from ClueLessGUI.ClueLess_Gameboard_Prototype import Ui_ClueGameBoard
from ClueLessGUI.login_window import Ui_ClueLoginWindow

class GameWindow(QtGui.QWindow):
    def __init__(self, parent=None):
        super(GameWindow, self).__init__(parent)

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QtCore.QSize(1464, 949))
        self.setMaximumSize(QtCore.QSize(1464, 949))
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

        self.clue_login_window.create_profile_button.clicked.connect(self.login_callback)
        self.clue_login_window.username_input_field.returnPressed.connect(
            self.clue_login_window.create_profile_button.click)

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
        print(f"TEXT entered: {self.clue_login_window.username_input_field.text()}")
        self.login_form_widget.hide()
        self.setCentralWidget(self.game_board_widget)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())