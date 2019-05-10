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
from PyQt5.QtCore import QCoreApplication, QUrl
import sys
import json
import traceback

class ClientNetworking:

    def __init__(self, Widget):
        self.widget = Widget
        self.base_url = "http://localhost:5000"
        self.net_manager = QtNetwork.QNetworkAccessManager()

    def get(self, path, callback):
        req = QtNetwork.QNetworkRequest(QUrl(self.base_url + path))
        self.net_manager.finished(callback)
        self.net_manager.get(req)

    def post_json(self, path, data: str, callback):
        req = QtNetwork.QNetworkRequest(QUrl(self.base_url + path))
        req.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/json")
        self.net_manager.finished.connect(callback)
        self.net_manager.post(req, data.encode('utf-8'))

    @staticmethod
    def reply_to_json(reply):
        """
        Converts an QNetworkReply objects data to JSON
        :param reply: QNetworkReply object (passed via connect())
        :return: dict()
        """
        er = reply.error()
        if er == QtNetwork.QNetworkReply.NoError:
            try:
                print(f"Error Code: {er}")
                bytes_string = reply.readAll()
                print(str(bytes_string, 'utf-8'))
                r_data = json.loads(str(bytes_string, 'utf-8'))
                print(f"Data as JSON/dict: {r_data}")
                return r_data, er
            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()
        return None, er








class Example:

    def __init__(self):
        print("test 1")
        self.doRequest()
        print("test 1")


    def doRequest(self):

        url = "http://localhost:5000/games/1/game_state"
        req = QtNetwork.QNetworkRequest(QUrl(url))

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)

    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            print(str(bytes_string, 'utf-8'))

        else:
            print("Error occured: ", er)
            print(reply.errorString())

        QCoreApplication.quit()

if __name__ == "__main__":
    app = QCoreApplication([])
    ex = Example()
    sys.exit(app.exec_())