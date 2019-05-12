from ClueLessGUI.ClueLessQTGUI import MainWindow
import sys
from multiprocessing import Process
import copy
from PyQt5 import QtWidgets


def create_gui_window():
    print("Creating windows")
    app = QtWidgets.QApplication(sys.argv)
    print(f"App: {id(app)}")
    main_window = MainWindow(app)
    print(f"Main window: {id(main_window)}")
    main_window.show()
    app.exec_()

if __name__ == "__main__":
    processes = []
    NUM_GUIS = 3 # CHANGE THIS FOR MORE OR LESS GUIS
    print("Starting gui")
    for i in range(NUM_GUIS):
        print(f"Starting GUI {i}")
        p = Process(target=create_gui_window)
        processes.append(p)
        p.start()

