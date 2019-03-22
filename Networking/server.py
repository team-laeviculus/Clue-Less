import flask
from flask import jsonify
import sqlite3
from flask_restful import Resource, Api

# Use dictionaries instead of lists for database returns
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class HandlePlayers(Resource):
    def get(self):
        conn = sqlite3.connect('players.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        all_players = cur.execute('SELECT * FROM players;').fetchall()
        return jsonify(all_players)


def go():
    app = flask.Flask(__name__)
    app.config["DEBUG"] = True
    api = Api(app)

    api.add_resource(HandlePlayers, '/players')
    app.run()

if __name__ == "__main__":
    go()
