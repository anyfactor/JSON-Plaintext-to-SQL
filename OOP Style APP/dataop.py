import sqlite3

class DatabaseInterface:
  '''
  Enters data to hardcoded path
  from a list of tuples
  '''
  def __init__(self):
    self.connection = sqlite3.connect('main test1.db')
    self.cursor = self.connection.cursor()
    self.create_table = ("CREATE TABLE IF NOT EXISTS posts"
                "(id INTEGER PRIMARY KEY, title text, score int,"
                " retrieved_on int, permalink text, over_18 int,"
                " num_comments int, post_id text,"
                " gilded int, full_link text,"
                " created_utc int, author text, url text)")

  def initialize_table(self):
    '''
    One time operation to create the table
    '''
    self.cursor.execute(self.create_table)
    self.connection.commit()
    return self.cursor

  def execute(self, query, data):
    '''
    Executes a executemany operation
    '''
    self.cursor.executemany(query, data)
    self.connection.commit()
    return self.cursor

  def db_operation_fn(self, data_for_db,):
    '''
    Inserts data into db
    '''
    query = ("INSERT INTO posts(title, score, retrieved_on, permalink,"
            "over_18, num_comments, post_id, gilded, full_link, created_utc, author, url) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?, ?)")
    return self.execute(query, data_for_db)
  
  def close_connection(self):
    self.connection.close()