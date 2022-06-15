import os
#import sqlite3
import psycopg2


import queue
q = queue.Queue()
def loop(conn):
    cur = conn.cursor()
    while True:
        my = []

        my.append(q.get())
        l=0
        while not q.empty() and l < 20:
            my.append(q.get())
            l+=1
        cur.execute("begin")
        cur.execute(' '.join(my)) # it already has a semicolon
        cur.execute("commit")
        #print(my)
        #print('queue', q.qsize())

class Table:
    def __init__(self, db, name, **columns):
        self.db = db
        self.name = name

        column_string = ""

        for col_name, col_type in columns.items():
            column_string += "\"" + col_name + "\" " + col_type + ","

        column_string = column_string[:-1]
        from threading import Thread
        Thread(target = loop, args = (self.db.db_connection,), daemon=True).start()

        # Create the table
        self.db.execute("""CREATE TABLE IF NOT EXISTS %s (%s)""" % (name, column_string))

    def insert_row(self, *values):
        """
        Inserts a new row into the SQLite Table
        :param values: The row values to be inserted
        """
        value_string = ""

        for value in values:
            value_string += "'" + str(value) + "',"

        value_string = value_string[:-1]

        q.put("""INSERT INTO %s VALUES (%s);""" % (self.name, value_string))



class SQLiteWrapper:
    """
    Wrapper class for handling interactions with a SQLite database.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.db_connection = None

    def open(self):
        """
        Attempts to open a connection to the SQLite Database.
        :raises sqlite3.Error if the program was unable to connect to the database
        """
        try:
            # If the user hasn't appended the 'sqlite' extension when specifying the file, go ahead and add it
            #if not self.db_name.endswith(""".sqlite"""):
            #    self.db_name += ".sqlite"

            self.db_connection = psycopg2.connect(self.db_name)
            self.cursor = self.db_connection.cursor()


            self.db_connection.isolation_level = None

        except psycopg2.Error as e:
            print("An error occurred while trying to connect to the SQLite Database.", e)
            raise e 

    def loop(self):
        pass

    def create_table(self, name, **columns):
        """
        Creates a new table in the SQLite Database.
        :param name: The name of the Table
        :param columns: A list of the columns present in the table, including their type
        """
        return Table(self, name, **columns)

    def execute(self, sql_str):
        """
        Executes a given SQLite string
        :param sql_str: A SQL statement to be sent to the SQLite database
        """


        ret = self.cursor.execute(sql_str)
        print("CREATE", ret)

    def begin(self):
        self.cursor.execute("begin")
        pass

    def commit(self):
        self.cursor.execute("commit")
        pass
