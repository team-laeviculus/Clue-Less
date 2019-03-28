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

    def testGetPlayers(self):
        print("Starting Get players test")
        response = self.app.get("/players", follow_redirects=True)
        r_data = response.get_json()
        print(f"Players: {r_data}")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # TAP: Not sure how to call the server to get the right function for this
    # def testGetPlayersByName(self, name):
    #     print("Starting Get Players By Name")
    #     response = self.app.get("/players", follow_redirects=True)
    #     r_data = response.get_json()
    #     print(f"Players: {r_data}")
    #     self.assertEqual(response.status_code, HTTPStatus.OK)

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
        #print(f"Players: {r.json['name']}")
        for k in r_data:
            print(f"{k}")
        print(f"Players: {r_data}")

        # Cleanup! We need to remove foobar!!!
        # TODO: Doesnt remove foobar... or there are a lot of players with the same name!
        r = self.app.delete(self.server_url + 'players', json=data)
        self.assertEqual(r.status_code, HTTPStatus.OK)

if __name__ == "__main__":

    print("Running tests...")
    unittest.main()
