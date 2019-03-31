import unittest
import pathlib
import os
import tempfile
from http import HTTPStatus

from Networking import server


class BasicServerTest(unittest.TestCase):
    """
    Setup and Teardown server. Run before and after each test case.
    """
    def setUp(self):
        print("Setting up test")
        server.app.config["TESTING"] = True
        server.app.config["DEBUG"] = False
        self.db_fd, server.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = server.app.test_client()
        self.server_url = "http://127.0.0.1:5000/"
        #TODO: Create test DB
        #TODO: Drop all tables in DB
        #TODO: Create table w/ columns in now empty DB
        """
        with server.app.app_context():
            server.init_db()
        """
        print("Starting tests...")
        self.assertEqual(server.app.debug, False)

    # Post test cleanup
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])


    """
    Test Case helper methods
    """

    # Helper method for adding players to db. Returns response
    def createPlayerHelper(self, player_data):
        print(f"Adding player: {player_data}")
        r = self.app.post(self.server_url + "players", json=player_data)
        return r

    def deletePlayerHelper(self, player_data):
        qry = f"/players/{player_data['name']}"
        r = self.app.delete(qry, json=player_data)
        return r


    """
    Test Cases
    """

    # Dummy test
    def test_root_query(self):
        print("Running GET Test")
        response = self.app.get("/", follow_redirects=True)
        r_data = response.get_json() # Decode the response data
        # j = response.get_json()
        print(f"Response: {r_data}")


        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(r_data["ROOT"], "Test")

    # Test unknown GET request - Expected Response codes: 404 NOT_FOUND, or BAD_REQUEST
    def testUnknownGetRequest(self):
        response = self.app.get("/foo/bar")
        print(f"Bad request status:  {response.status_code}")
        r_data = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    # Test for unhandled post requests
    def testUnknownPostRequest(self):
        response = self.app.post("/foo", data=dict({"hello": "world"}))
        r = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r, None)

    # Test get all players
    def testGetPlayers(self):
        print("Starting Get players test")
        response = self.app.get("/players", follow_redirects=True)
        r_data = response.get_json()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print(f'Players: ')
        for p in r_data:
            print(f"{p['name']}: {p}")

    # Test get an individual player that is already in the database
    def testGetValidPlayerByName(self):
        print("Starting Get Players By Name")
        # Create Fake  and insert it into the database
        fake_player = {'name': "DummyPlayer"}
        # r = self.app.post(self.server_url + "players", json=fake_player)
        r = self.createPlayerHelper(fake_player)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        # Get fake player
        response = self.app.get("/players/DummyPlayer", follow_redirects=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        r_data = response.get_json()
        print(f"Players: {r_data}")
        self.assertEqual(r_data.get('name'), "DummyPlayer")
        # self.assertEqual(response.status_code, HTTPStatus.OK)
        # Remove dummy player from DB
        r = self.app.delete(self.server_url + 'players', json=fake_player)
        self.assertEqual(r.status_code, HTTPStatus.OK)


    def testJoinGame(self):
        print("FooBar is going to try and join the game!")
        data = {'name': "FooBar"}
        r = self.app.post(self.server_url + "players", json=data)
        print(f"Join response code: {r.status_code}")
        self.assertEqual(r.status_code, HTTPStatus.OK)
        rd = r.get_json()
        print(f"Response data: {rd}")

        r = self.app.get("/players")
        r_data = r.get_json()

        #r = self.app.delete(self.server_url + 'players', json=data)
        #self.assertEqual(r.status_code, HTTPStatus.OK)
        print(f"Players: {r_data}")

    def testLeaveGameExistingPlayer(self):
        data = {'name': "TomTheCat"}
        r = self.createPlayerHelper(data)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        print(f"Response: {r.get_json()}")
        r = self.app.delete(self.server_url + 'players', json=data)

        print(f"Delete Response: {r.get_json()}")
        self.assertEqual(r.status_code, HTTPStatus.OK)

    def testDeleteExistingPlayer(self):
        data = {'name': "Jerry"}
        qry = "/players/" + data["name"]

        r = self.createPlayerHelper(data)
        self.assertEqual(r.status_code, HTTPStatus.OK)

        response = self.app.get(qry, follow_redirects=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        r = self.app.delete(qry, json=data)
        self.assertEqual(r.status_code, HTTPStatus.OK)

    def testDeleteNonExistingPlayer(self):
        data = {"name": "Doggo"}
        r = self.app.delete("/players/Doggo", json=data)
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)

    def testUpdateExistingPlayer(self):

        data = {'name': "DingDong"}
        qry = "/players/" + data['name']

        r = self.createPlayerHelper(data)
        self.assertEqual(r.status_code, HTTPStatus.OK)

        r = self.app.get(qry)
        self.assertEqual(r.status_code, HTTPStatus.OK)

        print(f"Inserting dangerous weapon into database")
        weapon_data = {"weapon": "tactical assault toothbrush"}
        r = self.app.put(qry, data=weapon_data)
        self.assertEqual(r.status_code, HTTPStatus.OK)

        r = self.app.get(qry)
        r_data = r.get_json()
        print(f"Data response: {data}")
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(r_data['weapon'], "tactical assault toothbrush")

        self.deletePlayerHelper(data)

    def testUpdateNonExistingPlayer(self):

        data = {'name': "Doggo"}
        qry = "/players/" + data['name']

        r = self.app.put(qry, data={"weapon": "tennis ball"})
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)



    # TODO: This wasnt as easy as I thought
    # def testGetPlayerAttribute(self):
    #     name = {'name': "DummyPlayer2"}
    #     self.createPlayerHelper(name)
    #
    #     qry = "/players/DummyPlayer2/weapon"
    #     r = self.app.get(qry)
    #     print(f"Atrtribute Response: {r.get_json()}")
    #     self.assertEqual(r.status_code, HTTPStatus.OK)
    #
    #     r = self.deletePlayerHelper(name)
    #     self.assertEqual(r.status_code, HTTPStatus.OK)





if __name__ == "__main__":

    print("Running tests...")
    unittest.main()
