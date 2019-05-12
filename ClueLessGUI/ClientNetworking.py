from PyQt5 import QtNetwork
from PyQt5.QtCore import QCoreApplication, QUrl, QTimer
import sys
import json
import traceback
import time


class ClientNetworking:

    def __init__(self, Widget):
        self.widget = Widget
        self.base_url = "http://localhost:5000"
        self.net_manager = QtNetwork.QNetworkAccessManager()
        self.server_status_timer = QTimer()
        self.game_id = 1

        self.status_callback = None

    def start_server_status_tick(self, tickrate=300):
        """
        Starts a timer which calls a HTTP get on status
        every <tickrate> ms
        :param tickrate: time in milliseconds
        :return:
        """
        self.server_status_timer.timeout.connect(self.get_server_status)
        self.server_status_timer.start(tickrate)

    def set_status_callback(self, function):
        self.status_callback = function

    def get_server_status(self):
        print(f"Getting Server Status on: /games/{self.game_id}/game_state")
        try:
            print(f"game_status tick")
            self.get(f"/games/{self.game_id}/game_state", self.status_callback)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

    def get(self, path, callback):
        print("\n")
        print("-"*100)
        print(f"GET {path}")
        req = QtNetwork.QNetworkRequest(QUrl(self.base_url + path))

        reply = self.net_manager.get(req)
        reply.finished.connect(lambda: callback(reply))

    def post_json(self, path, data: str, callback):
        req = QtNetwork.QNetworkRequest(QUrl(self.base_url + path))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json")
        reply = self.net_manager.post(req, data.encode('utf-8'))

        reply.finished.connect(lambda: callback(reply))

    def set_game_id(self, gid: str):
        self.game_id = gid

    def reply_to_json(self, reply):
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
                if reply.isFinished():
                    bytes_string = reply.readAll()
                    print(f"Data: {bytes_string}")
                    # print(str(bytes_string, 'utf-8'))
                    r_data = json.loads(str(bytes_string, 'utf-8')) if bytes_string else None
            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()
            finally:
                reply.close()
                reply.deleteLater()
        return r_data, er
