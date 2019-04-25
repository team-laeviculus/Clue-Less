import requests
import threading
from socketio import Client
from queue import Queue
from Logs.Logging import create_background_logger
import asyncio

class ClientSession:
    CLIENT_SESSION_INFO = None

class ClientNetworking(threading.Thread):
    log = create_background_logger("sio", "Logs")
    sio = Client(engineio_logger=log)
    inbound_q = None
    outbound_q = None

    # CLIENT_SESSION_INFO = None

    def __init__(self, url, name, inbound_q, outbound_q):
        threading.Thread.__init__(self)
        self.server_url = url
        self.name = name

    @staticmethod
    def set_message_queues(inbound_q: Queue, outbound_q: Queue):
        """
        Static method to set the message queues for the Client class object
        :param inbound_q: Queue for messages incoming from server
        :param outbound_q: Queue for messages to be sent to server
        :return:
        """
        ClientNetworking.inbound_q = inbound_q
        ClientNetworking.outbound_q = outbound_q

    @staticmethod
    def emit_message(event: str, data: dict, namespace: str = None, callback=None):
        ClientNetworking.sio.emit(event, data, namespace, callback)

    @staticmethod
    def broadcast_message(data: dict, namespace: str = None, callback=None):
        ClientNetworking.sio.send(data, namespace, callback)

    @staticmethod
    def sio_join_game(event: str, data: dict, namespace: str = None, callback=None):
        if not namespace and ClientSession.CLIENT_SESSION_INFO:
            namespace = ClientSession.CLIENT_SESSION_INFO['game']
            data = {} #todo
            ClientNetworking.sio.emit('new player', data)

    def run(self):

        """
        Main event loop for thread. all works goes here

        :return:
        """

        try:
            self.sio.connect(self.server_url)
            self.sio.emit('message', data={self.name: "Hello"})

        except Exception as e:
            print(f"An exception occurred: {e}")

    # socket-io tags receiving data must be marked static method

    @sio.on('join')
    def on_connect(self, data):
        print('connection established')
        print(f"SIO JOIN: {data}")
        # sio.emit('message', {'message': 'Hello World!'})
        # self.sio.emit('join', data={'username': 'Bob', 'room': "SuperAwesomeRoom"})
        # self.emit('chat message', data={
        #     'username': 'Bob',
        #     'room': "SuperAwesomeRoom",
        #     "message": "Hello everyone!!!!"
        # })
        # await sio.emit()

    @staticmethod
    @sio.on('message')
    def on_message(data):
        print('Message Received: ', data)
        ClientNetworking.inbound_q.put(data)

        # await sio.emit('my response', {'response': 'my response'})

    @staticmethod
    @sio.on('message', namespace='/games')
    def on_games_msg(data):
        """
        Currently the callback everything is using
        :param data:
        :return:
        """
        print(f"[CALLBACK] messsage: New message received for games")
        ClientNetworking.inbound_q.put(data)

    @staticmethod
    @sio.on('server reply')
    def on_server_reply(data):
        print(f"[CALLBACK: on_server_reply")
        ClientNetworking.inbound_q.put(data)
        # print(f"Queue empty? {ClientNetworking.inbound_q.empty()}")
        # print(f"Message Enqueued. Queue Size: {ClientNetworking.inbound_q.get()}")
        ClientNetworking.sio.emit('my response', {'response': 'my response'})
        # print(f"The Server Replied with: {data}")

    @staticmethod
    @sio.on('new player joined', namespace='/games')
    def on_new_player_message(data):
        print(f"[CALLBACK] NEW PLAYER JOINED message: {data}")
        ClientNetworking.inbound_q.put(data)

    @staticmethod
    @sio.on('game start', namespace='/games')
    def on_game_start(data):
        '''
        Data contains first players turn info. Client acts accordingly
        :param data:
        :return:
        '''
        print(f"[CALLBACK]: on_game_start: {data}")
        ClientNetworking.inbound_q.put(data)

    @staticmethod
    @sio.on('next players turn', namespace='/games')
    def on_next_players_turn(data):
        """
        Data contains player whose turn is up
        :param data:
        :return:
        """
        print(f"[CALLBACK]: on_next_players_turn: {data}")
        ClientNetworking.inbound_q.put(data)

    @staticmethod
    @sio.on('choose game token', namespace='/games')
    def on_choose_game_token(data):
        """
        Allow player to choose a game token. Should be on a one by one basis
        :return:
        """
        print(f"[CALLBACK]: on_choose_game_token: {data}")
        ClientNetworking.inbound_q.put(data)

class ClientNetworkHelper:
    """
    Helper Class
    """
    @staticmethod
    def create_message_for_server(event, data, namespace="/games"):
        payload = {
            "event": event,
            "namespace": namespace,
            "data": data
        }
        return payload



    # # @sio.on('join')
    # # async def join_a_room(username, roomname):
    # #     print(f"{username} joining room {roomname}")
    # #     return await sio.emit('join', data={'username': username, 'room': roomname})
    #
    # @sio.on('new player move')
    # def new_player_move(self, data):
    #     print(f"New room: {data}")
    #
    # @sio.on('disconnect')
    # def on_disconnect(self):
    #     print('disconnected from server')
    #
    # @sio.on('chat message')
    # def on_chat_message(self, data):
    #     print(f"Chat Message: {data}")



    def start_client(self):
        return self.sio.connect('http://localhost:5000')

    def get_all_players(self):
        r = requests.get(self.server_url + 'players')
        print(r.json())

    def join_game(self):
        print("Sending Join Request from ClientNetworking")
        data = {'name': self.name}
        r = requests.post(self.server_url + 'players', json=data)

    def leave_game(self):
        data = {'name': self.name}
        r = requests.delete(self.server_url + 'players', json=data)

  #  def end_game(self):
  #      r = requests.get(self.server_url + 'end_game')

if __name__ == "__main__":
    server_url = 'http://127.0.0.1:5000/'
    client = ClientNetworking(server_url, 'test_name', None, None)
    client.start()
    client.join()
    # client.get_all_players()
    # client.join_game()
    # client.get_all_players()
    # client.leave_game()
    # client.get_all_players()
