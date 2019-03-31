import sqlite3
import os


# Use dictionaries instead of lists for database returns
# This is optional
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


#TODO: add error handling for these class methods
#TODO: Might want this running in its own thread if we make server
# multithreaded (I think flask automatically handles multithreading)
class DBController:

    def __init__(self, db_path, port):
        self.db_path = db_path

        if not os.path.exists(self.db_path):
            print("Error: db not found")
            raise OSError

        self.port = port
        self.is_connected = False
        self.create_connection() # Temporarily For testing purposes


    # Connect to the database
    def create_connection(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False) #TODO: We will get a race condition
        self.conn.row_factory = dict_factory
        self.cur = self.conn.cursor()
        self.is_connected = True

    def create_table(self, table_name):
        pass

    def remove_table(self, table_name):
        pass

    # Get all values in the specified table
    def get_table_values(self, table_name):

        if not self.is_connected:
            self.create_connection()

        all_values = self.cur.execute('SELECT * FROM ' + table_name + ';').fetchall()
        return all_values

    # TAP: This should be correct, but hasn't been tested
    #  Get player in the player table by name
    def get_player_by_name(self, name):

        if not self.is_connected:
            self.create_connection()

        cur = self.conn.cursor()
        cur.execute("SELECT * FROM players WHERE name=?", (name,))
        rows = cur.fetchone()
        print(f"Player By Name Rows: {rows}")
        return rows

    def update_player_by_name(self, name, weapon=None, suspect=None, space=None):
        #TODO: Validate suspect exists before updating
        print(f"POST Request: Updating vals for {name}")
        player_info = self.get_player_by_name(name)
        if player_info:
            player = player_info['name']
            wep = player_info['weapon'] if weapon is None else weapon
            sus = player_info['suspect'] if suspect is None else suspect
            current_space = player_info['current_space'] if space is None else space
            player_id = player_info['ID']
            print(f"PUT Query: id={player_id}, player={player}, weapon={wep}, suspect={sus}, space={current_space}")

            self.cur.execute(f"UPDATE players SET weapon='{weapon}', suspect='{sus}', current_space='{current_space}' WHERE ID={player_id}")
            self.conn.commit()
    # Use this for deleting table items by player name
    def delete_player_by_name(self, name):
        player_v = self.get_player_by_name(name)
        print(f"Player Lookup Before Delete: {player_v}")
        if player_v:
            self.cur.execute(f"DELETE FROM players WHERE name=?", (name, ))
            self.conn.commit()
            print(f"Player Exists and was removed")
            return player_v
        print("Player Does not exist")
        return None

    # Add a value to a table
    def add_table_value(self, table_name, column_data):
        columns = '('
        values = []
        values_string = ' VALUES('
        for column, value in column_data.items():
            columns = columns + column + ','
            values.append(value)
            values_string = values_string + '? ,'

        #Remove trailing comma, add ending bracket
        columns = columns[:-1]
        columns = columns + ')'
        values_string = values_string[:-2]
        values_string = values_string + ')'
        command = 'INSERT INTO ' + table_name + columns + values_string
        self.cur.execute(command, values)
        self.conn.commit()

    def update_table_value(self, table_name, table_value):
        pass

    # Remove a value from a table.
    def remove_table_value(self, table_name, values):
        # TODO: Once table columns are defined, add params here
        params = 'name'
        command = 'DELETE FROM ' + table_name + ' WHERE ' + params + ' = ?'
        self.cur.execute(command, values)
        self.conn.commit()

    def disconnect(self):
        self.conn.close()
        self.is_connected = False