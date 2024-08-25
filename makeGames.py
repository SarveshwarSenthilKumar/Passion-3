import sqlite3
import os

os.remove("games.db")
connection = sqlite3.connect("games.db")
crsr = connection.cursor()
crsr.execute("CREATE TABLE games (id INTEGER, player1, player2, pickStr, pickStr2, date, game, turn, moves, PRIMARY KEY(id))")
connection.commit()
crsr.close()
connection.close()
test = open("games.db", "r")
test.close()