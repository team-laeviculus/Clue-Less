import flask
from flask import jsonify, request
import sqlite3
from flask_restful import Resource, Api

# Use dictionaries instead of lists for database returns
# This is optional
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Access to the player database
# Posts new players to the database, gets lists of all active players
class HandlePlayers(Resource):
    def get(self):
        conn = sqlite3.connect('../Databases/players.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        all_players = cur.execute('SELECT * FROM players;').fetchall()
        return jsonify(all_players)

    def post(self):
        conn = sqlite3.connect('../Databases/players.db')
        cur = conn.cursor()
        values = [request.json["name"]]
        command = 'INSERT INTO players(name) VALUES(?)'
        cur.execute(command, values)
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('../Databases/players.db')
        cur = conn.cursor()
        values = [request.json["name"]]
        command = 'DELETE FROM players WHERE name = ?'
        cur.execute(command, values)
        conn.commit()
        conn.close()

def end_game():
    return(jsonify("Ending Game"))

def go():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    api = Api(app)

    api.add_resource(HandlePlayers, '/players')
    api.add_resource(end_game, '/end_game')


    app.run()

if __name__ == "__main__":
    go()
