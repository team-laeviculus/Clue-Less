# import requests
# from http import HTTPStatus
# import threading
# import
# """
# Module for handling client network events for the GUI
# """
# class ClientNetworking:
#     def __init__(self, output_queue):
# BASE_URL="http://localhost:5000/"
# def create_profile(name: str):
#     url = BASE_URL + "games/players"
#     threading.Thread.run(requests.post, args=()
from PyQt5 import QtNetwork
from PyQt5.QtCore import QCoreApplication, QUrl, QTimer
import sys
import json
import traceback

class ClientNetworking:

    def __init__(self, Widget):
        self.widget = Widget
        self.base_url = "http://localhost:5000"
        self.net_manager = QtNetwork.QNetworkAccessManager()
        self.server_status_timer = QTimer()
        self.game_id = 0

    def start_server_status_tick(self, tickrate=300):
        """
        Starts a timer which calls a HTTP get on status
        every <tickrate> ms
        :param tickrate: time in milliseconds
        :return:
        """
        self.server_status_timer.timeout.connect(self.get_server_status)
        self.server_status_timer.start(1000)

    def get_server_status(self):
        try:
            print(f"game_status tick")
            self.get(f"/games/{self.game_id}/game_state", lambda data: print("Got some data"))
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

    def get(self, path, callback):
        req = QtNetwork.QNetworkRequest(QUrl(self.base_url + path))
        self.net_manager.finished.connect(callback)
        self.net_manager.get(req)

    def post_json(self, path, data: str, callback):
        req = QtNetwork.QNetworkRequest(QUrl(self.base_url + path))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json")
        self.net_manager.finished.connect(callback)
        self.net_manager.post(req, data.encode('utf-8'))

    def set_game_id(self, gid: str):
        self.game_id = gid

    @staticmethod
    def reply_to_json(reply):
        """
        Converts an QNetworkReply objects data to JSON
        :param reply: QNetworkReply object (passed via connect())
        :return: dict()
        """
        er = reply.error()
        r_data = None
        if er == QtNetwork.QNetworkReply.NoError:
            try:
                print(f"Error Code: {er}")
                # print(f"Error String: {QtNetwork.QNetworkReply.errorString()}")
                bytes_string = reply.readAll()
                print(str(bytes_string, 'utf-8'))
                r_data = json.loads(str(bytes_string, 'utf-8'))
                print(f"Data as JSON/dict: {r_data}")
            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()
        return r_data, er
