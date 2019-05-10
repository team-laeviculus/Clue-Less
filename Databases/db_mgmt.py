import sqlite3
from sqlite3 import Error
import random
import datetime
import sys
import traceback
import os


class CluelessDB:
    # Ensures Only a single instance of this class will exist over lifetime of the server

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(CluelessDB)
        return cls._instance

    # this class is used to create an empty database with 10 tables for the game
    def __init__(self, db_name='file::memory:?cache=shared'):
        try:
            print(f"CluelessDB object created")
            if not db_name:
                raise Exception("CluelessDB Exception - db_name cant be None")
            with sqlite3.connect(db_name, uri=True, check_same_thread=False) as conn:
                self.conn = conn
            # self.conn = sqlite3.connect('file::memory:', check_same_thread=False, uri=True)
            # self.conn = sqlite3.connect('game_data.db', check_same_thread=False)
            print(f"Conn info for new DB: {self.conn}")
        except Exception as e:
            print(f"DB Exception: {e}")
            traceback.print_exc()

# ------------------------------------------------------------------------------------------------------
# create tables

    def recreate_db(self, db_name='file::memory:?cache=shared'):
        try:
            self.conn = sqlite3.connect(db_name, uri=True, check_same_thread=False)
        except Error as e:
            print(e)
            traceback.print_exc()

    def create_all_tables(self):
        self.create_games_table()
        self.create_player_table()
        self.create_cards_table()
        self.create_notebook_table()
        self.create_case_file_table()
        self.create_suspect_table()
        self.create_weapon_table()
        self.create_room_table()
        self.create_suggest_log_table()
        self.create_accuse_log_table()

    def create_games_table(self):
        print("Trying to create games_table")
        print(f"CWD for DB: {os.getcwd()}")
        print(f"Connection Status: {self.conn}")
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS games''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS games(
        game_id INTEGER NOT NULL,
        player_id INTEGER NOT NULL, 
        createts TIMESTAMP NOT NULL)
        ''')
        c.close()

    def create_player_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS players''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS players(
        game_id INTEGER NOT NULL,
        name VARCHAR(20) NOT NULL, 
        player_no INTEGER NOT NULL, 
        createts TIMESTAMP NOT NULL,
        suspect_id INTEGER,
        active_turn INTEGER NOT NULL,
        location VARCHAR(20),
        num_suggest INTEGER NOT NULL,
        num_accuse INTEGER NOT NULL,
        last_suggest VARCHAR(20),
        last_accuse VARCHAR(20),
        connected INTEGER NOT NULL)
        ''')
        c.close()

    def create_cards_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS cards''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS cards(
        game_id INTEGER NOT NULL,
        card_id INTEGER NOT NULL,
        category VARCHAR(20) NOT NULL, 
        ref_id INTEGER NOT NULL, 
        name VARCHAR(20) NOT NULL,
        assign_to INTEGER)
        ''')
        c.close()

    def create_notebook_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS notebook''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS notebook(
        game_id INTEGER NOT NULL,
        player_id INTEGER NOT NULL, 
        card_id INTEGER NOT NULL,
        category VARCHAR(20) NOT NULL, 
        ref_id INTEGER NOT NULL,
        status INTEGER NOT NULL)
        ''')
        c.close()

    def create_case_file_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS case_file''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS case_file(
        game_id INTEGER NOT NULL,
        suspect_id INTEGER, 
        weapon_id INTEGER, 
        room_id INTEGER,
        solved INTEGER)
        ''')
        c.close()

    def create_suspect_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS suspect''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS suspect(
        game_id INTEGER NOT NULL,
        ref_id integer NOT NULL, 
        name VARCHAR(20) NOT NULL, 
        player_id INTEGER NOT NULL,
        location VARCHAR(20),
        case_match INTEGER NOT NULL)
        ''')
        c.close()

    def create_weapon_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS weapon''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS weapon(
        game_id INTEGER NOT NULL,
        ref_id integer NOT NULL, 
        name VARCHAR(20) NOT NULL, 
        location VARCHAR(20),
        case_match INTEGER NOT NULL)
        ''')
        c.close()

    def create_room_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS room''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS room(
        game_id INTEGER NOT NULL,
        ref_id integer NOT NULL, 
        name VARCHAR(20) NOT NULL,
        case_match INTEGER NOT NULL,
        door_blocked INTEGER NOT NULL)
        ''')
        c.close()

    def create_suggest_log_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS suggest_log''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS suggest_log(
        game_id INTEGER NOT NULL,
        suggest_string VARCHAR(20) NOT NULL, 
        player_id INTEGER NOT NULL, 
        createts TIMESTAMP NOT NULL,
        case_match INTEGER NOT NULL)
        ''')
        c.close()

    def create_accuse_log_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS accuse_log''')

        c.execute('''
        CREATE TABLE IF NOT EXISTS accuse_log(
        game_id INTEGER NOT NULL,
        accuse_string VARCHAR(20) NOT NULL, 
        player_id INTEGER NOT NULL, 
        createts TIMESTAMP NOT NULL,
        case_match INTEGER NOT NULL)
        ''')
        c.close()

# ------------------------------------------------------------------------------------------------------
# initialize tables

    def init_games(self, g_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM games WHERE game_id = ?", (g_id,))
        c.close()

    def init_players(self, g_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM players WHERE game_id = ?", (g_id,))
        c.close()

    def init_cards(self, g_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM cards WHERE game_id = ?", (g_id,))

        # Categories:  'S' = suspect, 'W' = weapon, 'R' = room
        # suspects: cards 1 - 6
        # weapons: cards 7 - 12
        # rooms:  cards 13 - 21

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 1, 'S', 1, (SELECT name FROM suspect WHERE ref_id = 1), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 2, 'S', 2, (SELECT name FROM suspect WHERE ref_id = 2), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 3, 'S', 3, (SELECT name FROM suspect WHERE ref_id = 3), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 4, 'S', 4, (SELECT name FROM suspect WHERE ref_id = 4), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 5, 'S', 5, (SELECT name FROM suspect WHERE ref_id = 5), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 6, 'S', 6, (SELECT name FROM suspect WHERE ref_id = 6), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 7, 'W', 1, (SELECT name FROM weapon WHERE ref_id = 1), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 8, 'W', 2, (SELECT name FROM weapon WHERE ref_id = 2), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 9, 'W', 3, (SELECT name FROM weapon WHERE ref_id = 3), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 10, 'W', 4, (SELECT name FROM weapon WHERE ref_id = 4), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 11, 'W', 5, (SELECT name FROM weapon WHERE ref_id = 5), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 12, 'W', 6, (SELECT name FROM weapon WHERE ref_id = 6), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 13, 'R', 1, (SELECT name FROM room WHERE ref_id = 1), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 14, 'R', 2, (SELECT name FROM room WHERE ref_id = 2), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 15, 'R', 3, (SELECT name FROM room WHERE ref_id = 3), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 16, 'R', 4, (SELECT name FROM room WHERE ref_id = 4), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 17, 'R', 5, (SELECT name FROM room WHERE ref_id = 5), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 18, 'R', 6, (SELECT name FROM room WHERE ref_id = 6), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 19, 'R', 7, (SELECT name FROM room WHERE ref_id = 7), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 20, 'R', 8, (SELECT name FROM room WHERE ref_id = 8), Null)", (g_id,))

        c.execute("INSERT INTO cards (game_id, card_id, category, ref_id, name, assign_to) "
                  "VALUES "
                  "(?, 21, 'R', 9, (SELECT name FROM room WHERE ref_id = 9), Null)", (g_id,))
        self.conn.commit()
        c.close()

    def init_notebook(self, g_id, player_no):
        c = self.conn.cursor()
        c.execute("DELETE FROM notebook WHERE player_id = ? and game_id = ?", (player_no, g_id,))

        # Categories:  'S' = suspect, 'W' = weapon, 'R' = room
        # Ref_ID for 'S'
        # Ref_ID for 'W'
        # Ref_ID for 'R'

        for s in range(1, 7):
            c.execute("INSERT INTO notebook (game_id, player_id, card_id, category, ref_id, status) "
                      "VALUES "
                      "(?, ?, ?, 'S', ?, 0)", (g_id, player_no, s, s,))

        for w in range(7, 13):
            c.execute("INSERT INTO notebook (game_id, player_id, card_id, category, ref_id, status) "
                      "VALUES "
                      "(?, ?, ?, 'W', ?, 0)", (g_id, player_no, w, w - 6,))

        for r in range(13, 22):
            c.execute("INSERT INTO notebook (game_id, player_id, card_id, category, ref_id, status) "
                      "VALUES "
                      "(?, ?, ?, 'R', ?, 0)", (g_id, player_no, r, r - 12,))
        self.conn.commit()
        c.close()

    def init_case_file(self, g_id, s, w, r):
        c = self.conn.cursor()
        c.execute("DELETE FROM case_file WHERE game_id = ?", (g_id,))

        # Categories:  'S' = suspect, 'W' = weapon, 'R' = room

        c.execute("INSERT INTO case_file (game_id, suspect_id, weapon_id, room_id, solved) "
                  "VALUES "
                  "(?, ?, ?, ?, 0)", (g_id, s, w, r))
        self.conn.commit()
        c.close()

        # TODO: IDK what these do, but update_weapons doesnt do anything right now
        self.update_suspects(g_id, s)
        self.update_weapons(g_id, w)
        self.update_rooms(g_id, r)

    def init_suspects(self, g_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM suspect WHERE game_id = ?", (g_id,))

        c.execute("INSERT INTO suspect (game_id, ref_id, name, player_id, location, case_match) "
                  "VALUES "
                  "(?, 1, 'Miss Scarlet', 0, ?, 0)", (g_id, None,))

        c.execute("INSERT INTO suspect (game_id, ref_id, name, player_id, location, case_match) "
                  "VALUES "
                  "(?, 2, 'Col Mustard', 0, ?, 0)", (g_id, None,))

        c.execute("INSERT INTO suspect (game_id, ref_id, name, player_id, location, case_match) "
                  "VALUES "
                  "(?, 3, 'Mrs. White', 0, ?, 0)", (g_id, None,))

        c.execute("INSERT INTO suspect (game_id, ref_id, name, player_id, location, case_match) "
                  "VALUES "
                  "(?, 4, 'Mr. Green', 0, ?, 0)", (g_id, None,))

        c.execute("INSERT INTO suspect (game_id, ref_id, name, player_id, location, case_match) "
                  "VALUES "
                  "(?, 5, 'Mrs. Peacock', 0, ?, 0)", (g_id, None,))

        c.execute("INSERT INTO suspect (game_id, ref_id, name, player_id, location, case_match) "
                  "VALUES "
                  "(?, 6, 'Prof. Plum', 0, ?, 0)", (g_id, None,))
        self.conn.commit()
        c.close()

    def init_weapons(self, g_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM weapon WHERE game_id = ?", (g_id,))

        c.execute("INSERT INTO weapon (game_id, ref_id, name, location, case_match) "
                  "VALUES "
                  "(?, 1, 'Candlestick', ?, 0)", (g_id, None,))

        c.execute("INSERT INTO weapon (game_id, ref_id, name, location, case_match) "
                  "VALUES "
                  "(?, 2, 'Knife', ?, 0)", (g_id, None,))

        c.execute("INSERT INTO weapon (game_id, ref_id, name, location, case_match) "
                  "VALUES "
                  "(?, 3, 'Lead Pipe', ?, 0)", (g_id, None,))

        c.execute("INSERT INTO weapon (game_id, ref_id, name, location, case_match) "
                  "VALUES "
                  "(?, 4, 'Revolver', ?, 0)", (g_id, None,))

        c.execute("INSERT INTO weapon (game_id, ref_id, name, location, case_match) "
                  "VALUES "
                  "(?, 5, 'Rope', ?, 0)", (g_id, None,))

        c.execute("INSERT INTO weapon (game_id, ref_id, name, location, case_match) "
                  "VALUES "
                  "(?, 6, 'Wrench', ?, 0)", (g_id, None,))
        self.conn.commit()
        c.close()

    def init_rooms(self, g_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM room WHERE game_id = ?", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 1, 'Lounge', 0, 0)", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 2, 'Dining Room', 0, 0)", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 3, 'Kitchen', 0, 0)", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 4, 'Ballroom', 0, 0)", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 5, 'Conservatory', 0, 0)", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 6, 'Library', 0, 0)", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 7, 'Study', 0, 0)", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 8, 'Hall', 0, 0)", (g_id,))

        c.execute("INSERT INTO room (game_id, ref_id, name, case_match, door_blocked) "
                  "VALUES "
                  "(?, 9, 'Billiard Room', 0, 0)", (g_id,))
        self.conn.commit()
        c.close()

    def init_suggest_log(self, g_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM suggest_log WHERE game_id = ?", (g_id,))
        c.close()

    def init_accuse_log(self, g_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM accuse_log WHERE game_id = ?", (g_id,))
        c.close()

# ------------------------------------------------------------------------------------------------------
# mod / update database tables

    def game_add(self, g_id, player_no, createts):
        c = self.conn.cursor()
        c.execute("INSERT INTO games (game_id, player_id, createts) "
                  "VALUES "
                  "(?, ?, ?)", (g_id, player_no, createts))
        self.conn.commit()
        c.close()

    def players_add(self, g_id, name, num, createts, s_id, active, loc, sug_cnt,
                    acc_cnt, last_sug, last_acc, con):
        c = self.conn.cursor()

        c.execute("INSERT INTO players (game_id, name, player_no, createts, suspect_id, "
                  "active_turn, location, num_suggest, num_accuse, last_suggest, "
                  "last_accuse, connected) "
                  "VALUES "
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (g_id, name, num, createts, s_id, active, loc, sug_cnt, acc_cnt, last_sug,
                   last_acc, con))

        c.execute("INSERT INTO games (game_id, player_id, createts) "
                  "VALUES "
                  "(?, ?, ?)",
                  (g_id, num, createts))
        self.conn.commit()
        c.close()

    def update_cards(self, g_id, cnum, assign):
        print((g_id, cnum, assign))
        c = self.conn.cursor()
        c.execute("UPDATE cards SET assign_to = ? WHERE card_id = ? and game_id = ?", (assign, cnum, g_id,))
        self.conn.commit()
        c.close()

    def check_cards(self, g_id, player_no, type_chk, val):
        c = self.conn.cursor()
        c.execute("SELECT name As CNT FROM cards WHERE assign_to = ? "
                  "and category = ? and name = ? and game_id = ?", (player_no, type_chk, val, g_id,))
        v = c.fetchone()
        print(str(v) + ':' + str(player_no) + ':' + type_chk + ':' + val + ':' + str(g_id))
        # print("Player " + str(player_no) + " disproved the suggestion with: " + str(v))
        ret_val = None
        if v is None:
            ret_val = None
        else:
            ret_val = v[0]
        c.close()
        return ret_val

    def update_suspects(self, g_id, cnum):
        c = self.conn.cursor()
        c.execute("UPDATE suspect SET case_match = 1 "
                  "WHERE ref_id = ? and game_id = ?", (cnum, g_id,))
        self.conn.commit()
        c.close()

    def update_weapons(self, g_id, cnum):
        pass
        #c = self.conn.cursor()
        #c.execute("UPDATE weapon SET case_match = 1 "
        #          "WHERE ref_id = ? and game_id = ?", (cnum - 6, g_id))
        #self.conn.commit()
        #c.close()

    def update_rooms(self, g_id, cnum):
        c = self.conn.cursor()
        c.execute("UPDATE room SET case_match = 1 "
                  "WHERE ref_id = ? and game_id = ?", (cnum - 12, g_id,))
        c.close()

    def update_notebook(self, g_id, cnum, player_no):
        c = self.conn.cursor()
        c.execute("UPDATE notebook SET status = 1 "
                  "WHERE player_id = ? and card_id = ? and game_id = ?", (player_no, cnum, g_id,))
        self.conn.commit()
        c.close()

    def suggest_log_add(self, g_id, suggest, player_no, datetime, match):
        c = self.conn.cursor()
        c.execute("INSERT INTO suggest_log (game_id, suggest_string, player_id, createts, case_match) "
                  "VALUES "
                  "(?, ?, ?, ?, ?)", (g_id, suggest, player_no, datetime, match,))
        self.conn.commit()
        c.close()

    def accuse_log_add(self, g_id, accuse, player_no, datetime, match):
        c = self.conn.cursor()
        c.execute("INSERT INTO accuse_log (game_id, accuse_string, player_id, createts, case_match) "
                  "VALUES "
                  "(?, ?, ?, ?, ?)", (g_id, accuse, player_no, datetime, match,))
        self.conn.commit()
        c.close()

# ------------------------------------------------------------------------------------------------------
# functions utilizing database tables

    def set_game_solution(self, g_id):
        # establish the solution for the game
        solution_s = random.randint(1, 6)
        solution_w = random.randint(7, 12)
        solution_r = random.randint(13, 21)

        # save to case file
        self.init_case_file(g_id, solution_s, solution_w, solution_r)

        # update suspect, weapon, & room table with solution results
        self.update_suspects(g_id, solution_s)
        self.update_weapons(g_id, solution_w)
        self.update_rooms(g_id, solution_r)

    def reset_notebooks(self, g_id, player_cnt):
        for p in range(1, player_cnt + 1):
            self.init_notebook(g_id, p)

    def shuffle_deal_cards(self, g_id, player_cnt, s_s, s_w, s_r):
        # shuffle the deck 3 times
        list_cards = [i for i in range(1,22)]
        random.shuffle(list_cards)
        print("List:  ", list_cards)

        random.shuffle(list_cards)
        print("List:  ", list_cards)

        random.shuffle(list_cards)
        print("List:  ", list_cards)

        # deal cards and save results in card and notebook tables
        player_num = 1  # start with player 1

        # c = self.conn.cursor()
        # c.execute("SELECT suspect_id FROM case_file WHERE game_id = ?", (g_id,))
        # sol_s = c.fetchone()[0]
        # c.execute("SELECT weapon_id FROM case_file WHERE game_id = ?", (g_id,))
        # sol_w = c.fetchone()[0]
        # c.execute("SELECT room_id FROM case_file WHERE game_id = ?", (g_id,))
        # sol_r = c.fetchone()[0]

        for d in range(0, len(list_cards)):
            print(list_cards[d])
            if list_cards[d] == s_s:
                self.update_cards(g_id, list_cards[d], 0)
            elif list_cards[d] == s_w:
                self.update_cards(g_id, list_cards[d], 0)
            elif list_cards[d] == s_r:
                self.update_cards(g_id, list_cards[d], 0)
            else:
                self.update_cards(g_id, list_cards[d], player_num)
                self.update_notebook(g_id, list_cards[d], player_num)
                if player_num != player_cnt:
                    player_num += 1
                else:
                    player_num = 1
            self.conn.commit()
            # c.close()

    def make_suggestion(self, g_id, player_num, player_cnt, suggest_suspect, suggest_weapon, suggest_room):
        # suggest_suspect = str(input("Please enter a suspect?"))
        # suggest_weapon = str(input("Please enter a weapon?"))
        # suggest_room = str(input("Please enter a room?"))

        # # temp items added so that test suggestions don't need to be typed
        # suggest_suspect = 'suspect1'
        # suggest_weapon = 'weapon3'
        # suggest_room = 'room4'
        self.update_player_location(suggest_suspect, suggest_room)
        active_player = player_num
        suggest_match = 1    # assume it is a match; attempt to disprove
        list_elements = ['S', 'W', 'R']

        # shuffle element list twice
        random.shuffle(list_elements)
        print("List:  ", list_elements)

        random.shuffle(list_elements)
        print("List:  ", list_elements)

        dt = datetime.datetime.now()

        ret_str = ''

        bRun = True

        for v in range(1, player_cnt + 1):
            print(str(v) + ' of ' + str(player_cnt))
            if v != active_player:
                for x in range(0, len(list_elements)):
                    if list_elements[x] == 'S':
                        result = self.check_cards(g_id, v, list_elements[x], suggest_suspect)
                    elif list_elements[x] == 'W':
                        result = self.check_cards(g_id, v, list_elements[x], suggest_weapon)
                    else:
                        result = self.check_cards(g_id, v, list_elements[x], suggest_room)
                    if result is not None:
                        suggest_match = 0
                        ret_str = "Player " + str(v) + " disproved the suggestion with: " + str(result)
                        bRun = False
                        break
                if bRun is False:
                    break

        if suggest_match == 0:
            self.suggest_log_add(g_id, suggest_suspect + ', ' + suggest_weapon + ', ' + suggest_room, active_player, dt, 0)
        else:
            self.suggest_log_add(g_id, suggest_suspect + ', ' + suggest_weapon + ', ' + suggest_room, active_player, dt, 1)
            ret_str = "None of the players were able to disprove the suggestion!"

        return ret_str

    def make_accusation(self, g_id, player_num, accuse_suspect, accuse_weapon, accuse_room):
        # # lines below are kept for test purposes only
        # accuse_suspect = 'suspect1'
        # accuse_weapon = 'weapon1'
        # accuse_room = 'room4'

        active_player = player_num
        accuse_match = 3  # assume it is a match; attempt to disprove; count down one for each category match

        dt = datetime.datetime.now()

        if self.check_cards(g_id, 0, 'S', accuse_suspect):
            accuse_match -= 1
            print(accuse_match)

        if self.check_cards(g_id, 0, 'W', accuse_weapon):
            accuse_match -= 1
            print(accuse_match)

        if self.check_cards(g_id,0, 'R', accuse_room):
            accuse_match -= 1
            print(accuse_match)

        if accuse_match > 0:
            self.accuse_log_add(g_id, accuse_suspect + ', ' + accuse_weapon + ', ' + accuse_room, active_player, dt, 0)
            ret_str = "Your accusation is NOT correct, you are no longer able to make accusations!!!"
        else:
            self.accuse_log_add(g_id, accuse_suspect + ', ' + accuse_weapon + ', ' + accuse_room, active_player, dt, 1)
            ret_str = "Your accusation is correct, you win the game!!!"

        return ret_str

    def put_player_in_game(self, name):
        c = self.conn.cursor()
        c.execute("SELECT COUNT(*) FROM games WHERE game_id = 1")  # get game player counts
        g1_player_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM games WHERE game_id = 2")
        g2_player_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM games WHERE game_id = 3")
        g3_player_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM games WHERE game_id = 4")
        g4_player_count = c.fetchone()[0]

        dt = datetime.datetime.now()
        if g1_player_count < 6:
            self.players_add(1, name, g1_player_count + 1, dt, g1_player_count + 1, 0, 'Library', 0, 0, None, None, 1)
            return 1, g1_player_count + 1
        elif g2_player_count < 6:
            self.players_add(2, name, g2_player_count + 1, dt, g2_player_count + 1, 0, 'Study', 0, 0, None, None, 1)
            return 2, g2_player_count + 1
        elif g3_player_count < 6:
            self.players_add(3, name, g3_player_count + 1, dt, g3_player_count + 1, 0, 'Kitchen', 0, 0, None, None, 1)
            return 3, g3_player_count + 1
        elif g4_player_count < 6:
            self.players_add(4, name, g4_player_count + 1, dt, g4_player_count + 1, 0, 'Kitchen', 0, 0, None, None, 1)
            return 4, g4_player_count + 1
        else:
            return 0, 0
    
    def get_player_cards(self, g_id, player_num):
        cur = self.conn.cursor()

        p_cards = cur.execute("SELECT card_id, category, name FROM cards "
                              "WHERE game_id = ? and assign_to = ?",
                              (g_id, player_num,)).fetchall()
        return p_cards
    
    def get_card_info(self, g_id, c_id):
        cur = self.conn.cursor()
        c_info = cur.execute("SELECT card_id, category, ref_id, name, assign_to FROM cards "
                              "WHERE game_id = ? and card_id = ?",
                              (g_id, c_id,)).fetchall()
        return c_info

    #  Get player in the player table by name
    def get_player_by_name(self, name):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM players WHERE name=?", (name,))
        rows = cur.fetchone()
        return rows

    #  Get player in the player table by location
    def get_player_by_location(self, location):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM players WHERE location=?", (location,))
        rows = cur.fetchall()
        return rows

    def get_player_location(self, name):
        cur = self.conn.cursor()
        cur.execute("SELECT location FROM players WHERE name=?", (name,))
        location = cur.fetchone()
        if location:
            return location[0] # A tuple is always returned, we just want the name
        return None

    # Get all values in the specified table
    def get_table_values(self, table_name):
        cur = self.conn.cursor()
        all_values = cur.execute('SELECT * FROM ' + table_name + ';').fetchall()
        return all_values

    # Get all values in the players db
    # TODO: After minimal, we may want to limit this information
    def get_game_state(self):
        return self.get_table_values("players")


    def update_player_location(self, name, location):
        c = self.conn.cursor()
        c.execute("UPDATE players SET location = ? "
                  "WHERE name = ?", (location, name))
        self.conn.commit()

        c.close()



    def update_active_turn(self, name):
        c = self.conn.cursor()
        c.execute("UPDATE players SET active_turn = '0' ")
        c.execute("UPDATE players SET active_turn = '1' "
                  "WHERE name = ?", (name,))
        self.conn.commit()

        c.close()
# ------------------------------------------------------------------------------------------------------
# functions utilizing database tables
# #below lines used for test purposes only

# test script



if __name__ == '__main__':
    db = CluelessDB()

# game setup
    test_game_num = 1

    # add new game
    db.create_games_table()
    # dt = datetime.datetime.now()
    # db.game_add(1, 0, dt)     # pass 0 initially for player_id

    # add suspects
    db.create_suspect_table()   # only run the line to the left when a new table is needed
    db.init_suspects(test_game_num)          # add suspects used for all games

    c = db.conn.cursor()  # only added to show results
    c.execute("SELECT * FROM suspect WHERE game_id = ?", (test_game_num,))
    print("suspect table: ")
    for row in c:
        print(row)
    c.close()

    # add weapons
    db.create_weapon_table()    # only run the line to the left when a new table is needed
    db.init_weapons(test_game_num)           # add weapons used for all games

    c = db.conn.cursor()  # only added to show results
    c.execute("SELECT * FROM weapon WHERE game_id = ?", (test_game_num,))
    print("weapon table: ")
    for row in c:
        print(row)
    c.close()

    # add rooms
    db.create_room_table()      # only run the line to the left when a new table is needed
    db.init_rooms(test_game_num)             # add rooms used for all games

    c = db.conn.cursor()  # only added to show results
    c.execute("SELECT * FROM room WHERE game_id = ?", (test_game_num,))
    print("room table: ")
    for row in c:
        print(row)
    c.close()

    # add players
    db.create_player_table()
    dt = datetime.datetime.now()

    db.put_player_in_game('Paul')
    db.put_player_in_game('Michael')
    db.put_player_in_game('Joshua')
    db.put_player_in_game('Taylor')
    db.put_player_in_game('Phillip')
    db.put_player_in_game('Daniel')

    c = db.conn.cursor()    # only added to show results
    c.execute("SELECT * FROM games WHERE game_id = ?", (test_game_num,))
    print("games table: " + str(c.fetchall()))
    c.execute("SELECT * FROM players WHERE game_id = ?", (test_game_num,))
    print("players table: " + str(c.fetchall()))
    c.close()

    # initialize cards for a game
    db.create_cards_table()
    db.init_cards(test_game_num)

    c = db.conn.cursor()       # only added to show results
    c.execute("SELECT * FROM cards WHERE game_id = ?", (test_game_num,))
    print("cards table: ")
    for row in c:
        print(row)
    c.close()

    # initialize notebooks
    db.create_notebook_table()          # only run the line to the left when a new table is needed
    c = db.conn.cursor()
    c.execute("SELECT COUNT(*) FROM games WHERE game_id = ?", (test_game_num,))
    player_count = c.fetchone()[0]
    for n in range(1, player_count + 1):
        db.init_notebook(test_game_num, n)
    c.close()

    c = db.conn.cursor()  # only added to show results
    c.execute("SELECT * FROM notebook WHERE game_id = ?", (test_game_num,))
    print("notebook table: ")
    for row in c:
        print(row)
    c.close()

    # initialize case file
    db.create_case_file_table()

    # establish the solution for a game
    solution_s = random.randint(1, 6)
    solution_w = random.randint(7, 12)
    solution_r = random.randint(13, 21)

    db.init_case_file(1, solution_s, solution_w, solution_r)

    c = db.conn.cursor()  # only added to show results
    c.execute("SELECT * FROM case_file WHERE game_id = ?", (test_game_num,))
    print("case file table: ")
    for row in c:
        print(row)
    c.close()

    # update suspect, weapon, & room table with solution results
    db.update_suspects(test_game_num, solution_s)
    db.update_weapons(test_game_num, solution_w)
    db.update_rooms(test_game_num, solution_r)

    # shuffle and deal cards
    db.shuffle_deal_cards(test_game_num, player_count, solution_s, solution_w, solution_r)

    c = db.conn.cursor()  # only added to show results
    c.execute("SELECT * FROM cards WHERE game_id = ?", (test_game_num,))
    print("cards table: ")
    for row in c:
        print(row)
    c.close()

    db.create_suggest_log_table()  # only do this at the beginning of the game
    db.create_accuse_log_table()  # only do this at the beginning of the game

# ------------------------------------------------------------------------------------------------------
# test area for suggestions and accusations

    test_player_num = 1
    test_player_cnt = 6

    msg = db.make_suggestion(test_game_num, test_player_num, test_player_cnt, "Miss Scarlet", "Lead Pipe", "Ballroom")
    print(msg)

    msg = db.make_accusation(test_game_num, test_player_num, "Miss Scarlet", "Lead Pipe", "Ballroom")
    print(msg)

    print(db.get_player_by_name('Paul'))
    print(db.get_player_location('Paul'))
    print(db.get_game_state())
    #
    print(db.get_player_by_location('Library'))
    db.update_player_location('Paul', 'Study')
    print(db.get_player_by_location('Study'))
    print('test okay')

    print(db.get_player_cards(1, 1))


