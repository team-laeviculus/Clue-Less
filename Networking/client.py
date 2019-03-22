import requests

class Client():

    def __init__(self, url, name):
        self.server_url = url
        self.name = name

    def get_all_players(self):
        r = requests.get(self.server_url + 'players')
        print(r.json())

    def join_game(self):
        data = {'name': self.name}
        r = requests.post(self.server_url + 'players', json=data)

    def leave_game(self):
        data = {'name': self.name}
        r = requests.delete(self.server_url + 'players', json=data)

  #  def end_game(self):
  #      r = requests.get(self.server_url + 'end_game')

if __name__ == "__main__":
    server_url = 'http://127.0.0.1:5000/'
    client = Client(server_url, 'test_name')
    client.get_all_players()
    client.join_game()
    client.get_all_players()
    client.leave_game()
    client.get_all_players()
