# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ClueLess_Gameboard_Prototype.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ClueGameBoard(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.setGeometry(QtCore.QRect(0, 0, 1464, 949))
        Widget.setMinimumSize(QtCore.QSize(1464, 949))
        Widget.setMaximumSize(QtCore.QSize(1464, 949))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        Widget.setFont(font)
        Widget.setAcceptDrops(False)
        Widget.setStyleSheet("background-color: rgb(38, 38, 38);")
        self.make_suggestion_button = QtWidgets.QPushButton(Widget)
        self.make_suggestion_button.setGeometry(QtCore.QRect(1210, 790, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.make_suggestion_button.setFont(font)
        self.make_suggestion_button.setStyleSheet("color: rgb(198, 198, 198);")
        self.make_suggestion_button.setObjectName("make_suggestion_button")
        self.make_accusation_button = QtWidgets.QPushButton(Widget)
        self.make_accusation_button.setGeometry(QtCore.QRect(1210, 860, 211, 51))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.make_accusation_button.setFont(font)
        self.make_accusation_button.setStyleSheet("color: rgb(198, 198, 198);")
        self.make_accusation_button.setObjectName("make_accusation_button")
        self.quit_game_button = QtWidgets.QPushButton(Widget)
        self.quit_game_button.setGeometry(QtCore.QRect(40, 870, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.quit_game_button.setFont(font)
        self.quit_game_button.setStyleSheet("color: rgb(179, 179, 179);")
        self.quit_game_button.setObjectName("quit_game_button")
        self.groupBox = QtWidgets.QGroupBox(Widget)
        self.groupBox.setGeometry(QtCore.QRect(1210, 20, 211, 731))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("color: rgb(216, 216, 216);")
        self.groupBox.setObjectName("groupBox")
        self.notebook_col_mustard = QtWidgets.QCheckBox(self.groupBox)
        self.notebook_col_mustard.setGeometry(QtCore.QRect(40, 30, 121, 20))
        self.notebook_col_mustard.setChecked(False)
        self.notebook_col_mustard.setObjectName("notebook_col_mustard")
        self.notebook_prof_plum = QtWidgets.QCheckBox(self.groupBox)
        self.notebook_prof_plum.setGeometry(QtCore.QRect(40, 60, 121, 20))
        self.notebook_prof_plum.setObjectName("notebook_prof_plum")
        self.notebook_mr_green = QtWidgets.QCheckBox(self.groupBox)
        self.notebook_mr_green.setGeometry(QtCore.QRect(40, 90, 121, 20))
        self.notebook_mr_green.setObjectName("notebook_mr_green")
        self.notebook_mrs_peacock = QtWidgets.QCheckBox(self.groupBox)
        self.notebook_mrs_peacock.setGeometry(QtCore.QRect(40, 120, 121, 20))
        self.notebook_mrs_peacock.setObjectName("notebook_mrs_peacock")
        self.notebook_miss_scarlet = QtWidgets.QCheckBox(self.groupBox)
        self.notebook_miss_scarlet.setGeometry(QtCore.QRect(40, 150, 121, 20))
        self.notebook_miss_scarlet.setObjectName("notebook_miss_scarlet")
        self.notebook_mrs_white = QtWidgets.QCheckBox(self.groupBox)
        self.notebook_mrs_white.setGeometry(QtCore.QRect(40, 180, 121, 20))
        self.notebook_mrs_white.setObjectName("notebook_mrs_white")
        self.checkBox_8 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_8.setGeometry(QtCore.QRect(40, 330, 121, 20))
        self.checkBox_8.setObjectName("checkBox_8")
        self.checkBox_9 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_9.setGeometry(QtCore.QRect(40, 240, 121, 20))
        self.checkBox_9.setChecked(False)
        self.checkBox_9.setObjectName("checkBox_9")
        self.checkBox_10 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_10.setGeometry(QtCore.QRect(40, 300, 121, 20))
        self.checkBox_10.setObjectName("checkBox_10")
        self.checkBox_11 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_11.setGeometry(QtCore.QRect(40, 390, 121, 20))
        self.checkBox_11.setObjectName("checkBox_11")
        self.checkBox_12 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_12.setGeometry(QtCore.QRect(40, 360, 121, 20))
        self.checkBox_12.setObjectName("checkBox_12")
        self.checkBox_13 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_13.setGeometry(QtCore.QRect(40, 270, 121, 20))
        self.checkBox_13.setObjectName("checkBox_13")
        self.checkBox_14 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_14.setGeometry(QtCore.QRect(40, 600, 121, 20))
        self.checkBox_14.setObjectName("checkBox_14")
        self.checkBox_15 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_15.setGeometry(QtCore.QRect(40, 570, 121, 20))
        self.checkBox_15.setObjectName("checkBox_15")
        self.checkBox_16 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_16.setGeometry(QtCore.QRect(40, 450, 121, 20))
        self.checkBox_16.setChecked(False)
        self.checkBox_16.setObjectName("checkBox_16")
        self.checkBox_17 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_17.setGeometry(QtCore.QRect(40, 480, 121, 20))
        self.checkBox_17.setObjectName("checkBox_17")
        self.checkBox_18 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_18.setGeometry(QtCore.QRect(40, 510, 121, 20))
        self.checkBox_18.setObjectName("checkBox_18")
        self.checkBox_19 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_19.setGeometry(QtCore.QRect(40, 540, 121, 20))
        self.checkBox_19.setObjectName("checkBox_19")
        self.checkBox_20 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_20.setGeometry(QtCore.QRect(40, 660, 121, 20))
        self.checkBox_20.setObjectName("checkBox_20")
        self.checkBox_21 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_21.setGeometry(QtCore.QRect(40, 630, 121, 20))
        self.checkBox_21.setObjectName("checkBox_21")
        self.checkBox_22 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_22.setGeometry(QtCore.QRect(40, 690, 121, 20))
        self.checkBox_22.setObjectName("checkBox_22")
        self.checkBox_23 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_23.setGeometry(QtCore.QRect(140, 630, 30, 20))
        self.checkBox_23.setText("")
        self.checkBox_23.setObjectName("checkBox_23")
        self.checkBox_24 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_24.setGeometry(QtCore.QRect(140, 480, 30, 20))
        self.checkBox_24.setText("")
        self.checkBox_24.setObjectName("checkBox_24")
        self.checkBox_25 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_25.setGeometry(QtCore.QRect(140, 600, 30, 20))
        self.checkBox_25.setText("")
        self.checkBox_25.setObjectName("checkBox_25")
        self.server_checkbox_mrs_white = QtWidgets.QCheckBox(self.groupBox)
        self.server_checkbox_mrs_white.setGeometry(QtCore.QRect(140, 180, 30, 20))
        self.server_checkbox_mrs_white.setText("")
        self.server_checkbox_mrs_white.setCheckable(False)
        self.server_checkbox_mrs_white.setObjectName("server_checkbox_mrs_white")
        self.checkBox_27 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_27.setGeometry(QtCore.QRect(140, 690, 30, 20))
        self.checkBox_27.setText("")
        self.checkBox_27.setObjectName("checkBox_27")
        self.checkBox_28 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_28.setGeometry(QtCore.QRect(140, 330, 30, 20))
        self.checkBox_28.setText("")
        self.checkBox_28.setObjectName("checkBox_28")
        self.server_checkbox_col_mustard = QtWidgets.QCheckBox(self.groupBox)
        self.server_checkbox_col_mustard.setGeometry(QtCore.QRect(140, 30, 30, 20))
        self.server_checkbox_col_mustard.setText("")
        self.server_checkbox_col_mustard.setCheckable(False)
        self.server_checkbox_col_mustard.setChecked(False)
        self.server_checkbox_col_mustard.setObjectName("server_checkbox_col_mustard")
        self.checkBox_30 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_30.setGeometry(QtCore.QRect(140, 510, 30, 20))
        self.checkBox_30.setText("")
        self.checkBox_30.setObjectName("checkBox_30")
        self.server_checkbox_miss_scarlet = QtWidgets.QCheckBox(self.groupBox)
        self.server_checkbox_miss_scarlet.setGeometry(QtCore.QRect(140, 150, 30, 20))
        self.server_checkbox_miss_scarlet.setText("")
        self.server_checkbox_miss_scarlet.setCheckable(False)
        self.server_checkbox_miss_scarlet.setObjectName("server_checkbox_miss_scarlet")
        self.server_checkbox_mrs_peacock = QtWidgets.QCheckBox(self.groupBox)
        self.server_checkbox_mrs_peacock.setGeometry(QtCore.QRect(140, 120, 30, 20))
        self.server_checkbox_mrs_peacock.setText("")
        self.server_checkbox_mrs_peacock.setCheckable(False)
        self.server_checkbox_mrs_peacock.setObjectName("server_checkbox_mrs_peacock")
        self.checkBox_33 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_33.setGeometry(QtCore.QRect(140, 660, 30, 20))
        self.checkBox_33.setText("")
        self.checkBox_33.setObjectName("checkBox_33")
        self.checkBox_34 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_34.setGeometry(QtCore.QRect(140, 390, 30, 20))
        self.checkBox_34.setText("")
        self.checkBox_34.setObjectName("checkBox_34")
        self.checkBox_35 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_35.setGeometry(QtCore.QRect(140, 540, 30, 20))
        self.checkBox_35.setText("")
        self.checkBox_35.setObjectName("checkBox_35")
        self.checkBox_36 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_36.setGeometry(QtCore.QRect(140, 570, 30, 20))
        self.checkBox_36.setText("")
        self.checkBox_36.setObjectName("checkBox_36")
        self.server_checkbox_mr_green = QtWidgets.QCheckBox(self.groupBox)
        self.server_checkbox_mr_green.setGeometry(QtCore.QRect(140, 90, 30, 20))
        self.server_checkbox_mr_green.setText("")
        self.server_checkbox_mr_green.setCheckable(False)
        self.server_checkbox_mr_green.setObjectName("server_checkbox_mr_green")
        self.checkBox_38 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_38.setGeometry(QtCore.QRect(140, 270, 30, 20))
        self.checkBox_38.setText("")
        self.checkBox_38.setObjectName("checkBox_38")
        self.checkBox_39 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_39.setGeometry(QtCore.QRect(140, 450, 30, 20))
        self.checkBox_39.setText("")
        self.checkBox_39.setChecked(False)
        self.checkBox_39.setObjectName("checkBox_39")
        self.checkBox_40 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_40.setGeometry(QtCore.QRect(140, 360, 30, 20))
        self.checkBox_40.setText("")
        self.checkBox_40.setObjectName("checkBox_40")
        self.checkBox_41 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_41.setGeometry(QtCore.QRect(140, 240, 30, 20))
        self.checkBox_41.setText("")
        self.checkBox_41.setChecked(False)
        self.checkBox_41.setObjectName("checkBox_41")
        self.server_checkbox_prof_plum = QtWidgets.QCheckBox(self.groupBox)
        self.server_checkbox_prof_plum.setGeometry(QtCore.QRect(140, 60, 30, 20))
        self.server_checkbox_prof_plum.setText("")
        self.server_checkbox_prof_plum.setCheckable(False)
        self.server_checkbox_prof_plum.setObjectName("server_checkbox_prof_plum")
        self.checkBox_43 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_43.setGeometry(QtCore.QRect(140, 300, 30, 20))
        self.checkBox_43.setText("")
        self.checkBox_43.setObjectName("checkBox_43")
        self.groupBox_2 = QtWidgets.QGroupBox(Widget)
        self.groupBox_2.setGeometry(QtCore.QRect(300, 20, 881, 691))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setAcceptDrops(True)
        self.groupBox_2.setStyleSheet("color: rgb(186, 186, 186);")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(70, 30, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgb(170, 170, 127);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_4.setIndent(2)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(350, 30, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("background-color: rgb(85, 255, 255);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_5.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_5.setIndent(2)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(630, 30, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background-color: rgb(255, 170, 0);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_6.setIndent(2)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(630, 270, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background-color: rgb(255, 255, 127);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_7.setIndent(2)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(70, 270, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color: rgb(170, 85, 127);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_8.setIndent(2)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(350, 270, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color: rgb(0, 170, 127);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_9.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_9.setIndent(2)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(630, 510, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.label_10.setIndent(2)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(70, 510, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_11.setIndent(2)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(350, 510, 191, 161))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"border: 1px solid black;\n"
"color: rgb(0, 0, 0);")
        self.label_12.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_12.setIndent(2)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(260, 70, 91, 81))
        self.label_13.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setGeometry(QtCore.QRect(540, 70, 91, 81))
        self.label_14.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_14.setText("")
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setGeometry(QtCore.QRect(260, 310, 91, 81))
        self.label_15.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_15.setText("")
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox_2)
        self.label_16.setGeometry(QtCore.QRect(540, 310, 91, 81))
        self.label_16.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_16.setText("")
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.groupBox_2)
        self.label_17.setGeometry(QtCore.QRect(260, 550, 91, 81))
        self.label_17.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_17.setText("")
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.groupBox_2)
        self.label_18.setGeometry(QtCore.QRect(540, 550, 91, 81))
        self.label_18.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_18.setText("")
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.groupBox_2)
        self.label_19.setGeometry(QtCore.QRect(120, 430, 91, 81))
        self.label_19.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_19.setText("")
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.groupBox_2)
        self.label_20.setGeometry(QtCore.QRect(120, 190, 91, 81))
        self.label_20.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_20.setText("")
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.groupBox_2)
        self.label_21.setGeometry(QtCore.QRect(400, 190, 91, 81))
        self.label_21.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_21.setText("")
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.groupBox_2)
        self.label_22.setGeometry(QtCore.QRect(400, 430, 91, 81))
        self.label_22.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_22.setText("")
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(self.groupBox_2)
        self.label_23.setGeometry(QtCore.QRect(680, 190, 91, 81))
        self.label_23.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_23.setText("")
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.groupBox_2)
        self.label_24.setGeometry(QtCore.QRect(680, 430, 91, 81))
        self.label_24.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.label_24.setText("")
        self.label_24.setObjectName("label_24")
        self.label_31 = QtWidgets.QLabel(self.groupBox_2)
        self.label_31.setGeometry(QtCore.QRect(280, 90, 51, 41))
        self.label_31.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_31.setText("")
        self.label_31.setPixmap(QtGui.QPixmap("Assets/blue_game_piece.png"))
        self.label_31.setScaledContents(True)
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.groupBox_2)
        self.label_32.setGeometry(QtCore.QRect(560, 90, 51, 41))
        self.label_32.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_32.setText("")
        self.label_32.setPixmap(QtGui.QPixmap("Assets/red_game_piece.png"))
        self.label_32.setScaledContents(True)
        self.label_32.setObjectName("label_32")
        self.label_33 = QtWidgets.QLabel(self.groupBox_2)
        self.label_33.setGeometry(QtCore.QRect(280, 570, 51, 41))
        self.label_33.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_33.setText("")
        self.label_33.setPixmap(QtGui.QPixmap("Assets/purple_game_piece.png"))
        self.label_33.setScaledContents(True)
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.groupBox_2)
        self.label_34.setGeometry(QtCore.QRect(560, 570, 51, 41))
        self.label_34.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_34.setText("")
        self.label_34.setPixmap(QtGui.QPixmap("Assets/yellow_game_piece.png"))
        self.label_34.setScaledContents(True)
        self.label_34.setObjectName("label_34")
        self.label_35 = QtWidgets.QLabel(self.groupBox_2)
        self.label_35.setGeometry(QtCore.QRect(80, 610, 61, 51))
        self.label_35.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_35.setText("")
        self.label_35.setPixmap(QtGui.QPixmap("Assets/candlestick_game_piece.png"))
        self.label_35.setScaledContents(True)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.groupBox_2)
        self.label_36.setGeometry(QtCore.QRect(400, 610, 61, 51))
        self.label_36.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_36.setText("")
        self.label_36.setPixmap(QtGui.QPixmap("Assets/knife_game_piece.png"))
        self.label_36.setScaledContents(True)
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.groupBox_2)
        self.label_37.setGeometry(QtCore.QRect(760, 620, 51, 41))
        self.label_37.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_37.setText("")
        self.label_37.setPixmap(QtGui.QPixmap("Assets/lead_pipe_game_piece.png"))
        self.label_37.setScaledContents(True)
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.groupBox_2)
        self.label_38.setGeometry(QtCore.QRect(770, 130, 41, 51))
        self.label_38.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_38.setText("")
        self.label_38.setPixmap(QtGui.QPixmap("Assets/rope_game_piece.png"))
        self.label_38.setScaledContents(True)
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.groupBox_2)
        self.label_39.setGeometry(QtCore.QRect(420, 150, 51, 31))
        self.label_39.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_39.setText("")
        self.label_39.setPixmap(QtGui.QPixmap("Assets/revolver_game_piece.png"))
        self.label_39.setScaledContents(True)
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.groupBox_2)
        self.label_40.setGeometry(QtCore.QRect(80, 150, 61, 31))
        self.label_40.setAcceptDrops(True)
        self.label_40.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_40.setText("")
        self.label_40.setPixmap(QtGui.QPixmap("Assets/wrench_game_piece.png"))
        self.label_40.setScaledContents(True)
        self.label_40.setObjectName("label_40")
        self.label_41 = QtWidgets.QLabel(self.groupBox_2)
        self.label_41.setGeometry(QtCore.QRect(140, 450, 51, 41))
        self.label_41.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_41.setText("")
        self.label_41.setPixmap(QtGui.QPixmap("Assets/green_game_piece.png"))
        self.label_41.setScaledContents(True)
        self.label_41.setObjectName("label_41")
        self.label_42 = QtWidgets.QLabel(self.groupBox_2)
        self.label_42.setGeometry(QtCore.QRect(700, 210, 51, 41))
        self.label_42.setStyleSheet("background-color: rgba(0, 0, 0, 0%);")
        self.label_42.setText("")
        self.label_42.setPixmap(QtGui.QPixmap("Assets/orange_game_piece.png"))
        self.label_42.setScaledContents(True)
        self.label_42.setObjectName("label_42")
        self.label_24.raise_()
        self.label_23.raise_()
        self.label_21.raise_()
        self.label_22.raise_()
        self.label_19.raise_()
        self.label_20.raise_()
        self.label_18.raise_()
        self.label_17.raise_()
        self.label_16.raise_()
        self.label_15.raise_()
        self.label_14.raise_()
        self.label_13.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_31.raise_()
        self.label_32.raise_()
        self.label_33.raise_()
        self.label_34.raise_()
        self.label_35.raise_()
        self.label_36.raise_()
        self.label_37.raise_()
        self.label_38.raise_()
        self.label_39.raise_()
        self.label_40.raise_()
        self.label_41.raise_()
        self.label_42.raise_()
        self.game_status_window = QtWidgets.QLabel(Widget)
        self.game_status_window.setGeometry(QtCore.QRect(350, 720, 831, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.game_status_window.setFont(font)
        self.game_status_window.setAutoFillBackground(False)
        self.game_status_window.setStyleSheet("background-color: rgb(156, 156, 156);\n"
"border: 1px solid black;")
        self.game_status_window.setIndent(2)
        self.game_status_window.setObjectName("game_status_window")
        self.groupBox_3 = QtWidgets.QGroupBox(Widget)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 20, 251, 731))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet("color: rgb(198, 198, 198);")
        self.groupBox_3.setObjectName("groupBox_3")
        self.chat_text_display_box = QtWidgets.QLabel(self.groupBox_3)
        self.chat_text_display_box.setGeometry(QtCore.QRect(10, 30, 231, 691))
        self.chat_text_display_box.setAutoFillBackground(False)
        self.chat_text_display_box.setStyleSheet("background-color: rgb(170, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.chat_text_display_box.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.chat_text_display_box.setWordWrap(True)
        self.chat_text_display_box.setIndent(2)
        self.chat_text_display_box.setObjectName("chat_text_display_box")
        self.message_input_text_box = QtWidgets.QTextEdit(Widget)
        self.message_input_text_box.setGeometry(QtCore.QRect(30, 760, 251, 31))
        self.message_input_text_box.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 127);")
        self.message_input_text_box.setInputMethodHints(QtCore.Qt.ImhNone)
        self.message_input_text_box.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.message_input_text_box.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.message_input_text_box.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.message_input_text_box.setObjectName("message_input_text_box")
        self.send_message_button = QtWidgets.QPushButton(Widget)
        self.send_message_button.setGeometry(QtCore.QRect(30, 800, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.send_message_button.setFont(font)
        self.send_message_button.setStyleSheet("color: rgb(203, 203, 203);")
        self.send_message_button.setObjectName("send_message_button")
        self.card_1 = QtWidgets.QLabel(Widget)
        self.card_1.setGeometry(QtCore.QRect(300, 760, 131, 151))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.card_1.setFont(font)
        self.card_1.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"color: rgb(0, 0, 0);\n"
"border: 1px solid brown;")
        self.card_1.setTextFormat(QtCore.Qt.AutoText)
        self.card_1.setAlignment(QtCore.Qt.AlignCenter)
        self.card_1.setObjectName("card_1")
        self.card_2 = QtWidgets.QLabel(Widget)
        self.card_2.setGeometry(QtCore.QRect(450, 760, 131, 151))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.card_2.setFont(font)
        self.card_2.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"color: rgb(0, 0, 0);\n"
"border: 1px solid brown;")
        self.card_2.setAlignment(QtCore.Qt.AlignCenter)
        self.card_2.setObjectName("card_2")
        self.card_3 = QtWidgets.QLabel(Widget)
        self.card_3.setGeometry(QtCore.QRect(600, 760, 131, 151))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.card_3.setFont(font)
        self.card_3.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"color: rgb(0, 0, 0);\n"
"border: 1px solid brown;")
        self.card_3.setAlignment(QtCore.Qt.AlignCenter)
        self.card_3.setObjectName("card_3")
        self.card_4 = QtWidgets.QLabel(Widget)
        self.card_4.setGeometry(QtCore.QRect(750, 760, 131, 151))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.card_4.setFont(font)
        self.card_4.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"color: rgb(0, 0, 0);\n"
"border: 1px solid brown;")
        self.card_4.setAlignment(QtCore.Qt.AlignCenter)
        self.card_4.setObjectName("card_4")
        self.card_5 = QtWidgets.QLabel(Widget)
        self.card_5.setGeometry(QtCore.QRect(900, 760, 131, 151))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.card_5.setFont(font)
        self.card_5.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"color: rgb(0, 0, 0);\n"
"border: 1px solid brown;")
        self.card_5.setAlignment(QtCore.Qt.AlignCenter)
        self.card_5.setObjectName("card_5")
        self.card_6 = QtWidgets.QLabel(Widget)
        self.card_6.setGeometry(QtCore.QRect(1050, 760, 131, 151))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        self.card_6.setFont(font)
        self.card_6.setStyleSheet("background-color: rgb(255, 170, 127);\n"
"color: rgb(0, 0, 0);\n"
"border: 1px solid brown;")
        self.card_6.setAlignment(QtCore.Qt.AlignCenter)
        self.card_6.setObjectName("card_6")
        self.label_43 = QtWidgets.QLabel(Widget)
        self.label_43.setGeometry(QtCore.QRect(300, 720, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        self.label_43.setFont(font)
        self.label_43.setAutoFillBackground(False)
        self.label_43.setStyleSheet("background-color: rgb(156, 156, 156);\n"
"border: 1px solid black;")
        self.label_43.setText("")
        self.label_43.setIndent(2)
        self.label_43.setObjectName("label_43")

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("ClueGameBoard", "ClueLess by Team Laeviculus"))
        self.make_suggestion_button.setText(_translate("ClueGameBoard", "Make Suggestion"))
        self.make_accusation_button.setText(_translate("ClueGameBoard", "Make Accusation"))
        self.quit_game_button.setText(_translate("ClueGameBoard", "Quit Game"))
        self.groupBox.setTitle(_translate("ClueGameBoard", "Player 1 Notebook"))
        self.notebook_col_mustard.setText(_translate("ClueGameBoard", "Col. Mustard"))
        self.notebook_prof_plum.setText(_translate("ClueGameBoard", "Prof. Plum"))
        self.notebook_mr_green.setText(_translate("ClueGameBoard", "Mr. Green"))
        self.notebook_mrs_peacock.setText(_translate("ClueGameBoard", "Mrs. Peacock"))
        self.notebook_miss_scarlet.setText(_translate("ClueGameBoard", "Miss Scarlet"))
        self.notebook_mrs_white.setText(_translate("ClueGameBoard", "Mrs. White"))
        self.checkBox_8.setText(_translate("ClueGameBoard", "Weapon 1"))
        self.checkBox_9.setText(_translate("ClueGameBoard", "Weapon 1"))
        self.checkBox_10.setText(_translate("ClueGameBoard", "Weapon 1"))
        self.checkBox_11.setText(_translate("ClueGameBoard", "Weapon 1"))
        self.checkBox_12.setText(_translate("ClueGameBoard", "Weapon 1"))
        self.checkBox_13.setText(_translate("ClueGameBoard", "Weapon 1"))
        self.checkBox_14.setText(_translate("ClueGameBoard", "Room 1"))
        self.checkBox_15.setText(_translate("ClueGameBoard", "Room 1"))
        self.checkBox_16.setText(_translate("ClueGameBoard", "Room 1"))
        self.checkBox_17.setText(_translate("ClueGameBoard", "Room 1"))
        self.checkBox_18.setText(_translate("ClueGameBoard", "Room 1"))
        self.checkBox_19.setText(_translate("ClueGameBoard", "Room 1"))
        self.checkBox_20.setText(_translate("ClueGameBoard", "Room 1"))
        self.checkBox_21.setText(_translate("ClueGameBoard", "Room 1"))
        self.checkBox_22.setText(_translate("ClueGameBoard", "Room 1"))
        self.groupBox_2.setTitle(_translate("ClueGameBoard", "Gameboard"))
        self.label_4.setText(_translate("ClueGameBoard", "Study"))
        self.label_5.setText(_translate("ClueGameBoard", "Hall"))
        self.label_6.setText(_translate("ClueGameBoard", "Lounge"))
        self.label_7.setText(_translate("ClueGameBoard", "Dining Room"))
        self.label_8.setText(_translate("ClueGameBoard", "Library"))
        self.label_9.setText(_translate("ClueGameBoard", "Billiard Room"))
        self.label_10.setText(_translate("ClueGameBoard", "Kitchen"))
        self.label_11.setText(_translate("ClueGameBoard", "Conservatory"))
        self.label_12.setText(_translate("ClueGameBoard", "Ballroom"))
        self.game_status_window.setText(_translate("ClueGameBoard", "Waiting for game..."))
        self.groupBox_3.setTitle(_translate("ClueGameBoard", "Messages"))
        self.chat_text_display_box.setText(_translate("ClueGameBoard", "Greetings !!!....Welcome to ClueLess"))
        self.send_message_button.setText(_translate("ClueGameBoard", "Send"))
        self.card_1.setText(_translate("ClueGameBoard", "Col Mustard"))
        self.card_2.setText(_translate("ClueGameBoard", "Prof Plum"))
        self.card_3.setText(_translate("ClueGameBoard", "Lead Pipe"))
        self.card_4.setText(_translate("ClueGameBoard", "Revolver"))
        self.card_5.setText(_translate("ClueGameBoard", "Library"))
        self.card_6.setText(_translate("ClueGameBoard", "Study"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget = QtWidgets.QWidget()
    ui = Ui_ClueGameBoard()
    ui.setupUi(Widget)
    Widget.show()
    sys.exit(app.exec_())

