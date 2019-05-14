from PyQt5 import QtNetwork
from PyQt5.QtCore import QCoreApplication, QUrl, QTimer
import sys
import json
import traceback
import time
from functools import partial


class ClientNetworking:

    def __init__(self, Widget):
        self.game_board_widget = Widget
        self.base_url = "http://localhost:5000"
        self.net_manager = QtNetwork.QNetworkAccessManager()
        self.server_status_timer = QTimer()
        self.game_id = 1
        self.profile_data = None
        self.status_callback = None

        self.status_box_update_fp = self.game_board_widget.update_game_status

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

    def set_profile_data(self, data):
        print(f"Profile name updated from {self.profile_data} to {data}")
        self.profile_data = data

    def get_server_status(self):
        print(f"Getting Server Status on: /games/{self.game_id}/game_state")
        try:
            print(f"game_status tick")
            self.get(f"/games/{self.game_id}/game_state", self.status_callback)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()

    def get_my_cards(self, callback):
        """
        Gets the cards for this client (using the set profile name).
        :return: list of card tuples: [(card_id, card_type, card_info)] or None if there was an error
        """
        print(f"Getting Cards from the server")
        try:
            self.get(f"/games/{self.game_id}/{self.profile_data['name']}/cards", callback)
        except Exception as e:
            print(f"get_my_cards exception: {e}")
            traceback.print_exc()

    def get_connected_rooms(self):
        current_room = self.game_board_widget.my_profile['location']
        if current_room:
            try:
                print(f"GETTING CONNECTED ROOMS")
                self.get(f"/games/{self.game_id}/connected/{current_room}",
                         self.__get_connected_rooms_callback
                         )
            except Exception as e:
                print(f"get_connected_rooms exception: {e}")
                traceback.print_exc()

    def __get_connected_rooms_callback(self, reply):
        data, er = self.reply_to_json(reply)
        if er == QtNetwork.QNetworkReply.NoError:
            print(f"get_connected_rooms data: {data}")
            if 'connected' in data:
                self.game_board_widget.add_message_to_chat_window(f"Connected Rooms: {data['connected']}")
                self.game_board_widget.make_move_callback(data['connected'])
            return data
        elif er == 400:
            print(f"get_connected_rooms 400 Response!")
            if data and 'error' in data:
                data_holder = data
                self.status_box_update_fp(f"Error! {data['error']}")
        else:
            print(f"get_connected_rooms Unhandled error type: {er}")
            self.status_box_update_fp(f"Unhandled networking error type: {er}")
        return None


    def get(self, path, callback):
        print(f"\n")
        print("-"*100)
        print(f"GET {path}")
        try:
            req = QtNetwork.QNetworkRequest(QUrl(self.base_url + path))

            reply = self.net_manager.get(req)
            print(f"GET Callback: {callback}")
            reply.finished.connect(lambda: callback(reply))
        except Exception as e:
            print(f"GET Exception! {e}")
            traceback.print_exc()

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
        print(f"ERROR: {er}")
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
        else:
            print("[reply_to_json]: An error occured!")
        return r_data, er
