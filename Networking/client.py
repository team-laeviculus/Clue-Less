import requests

server_url = 'http://127.0.0.1:5000/'

def get_all_players():
    r = requests.get(server_url + 'players')
    print(r.url)
    print(r.json())

if __name__ == "__main__":
    get_all_players()
