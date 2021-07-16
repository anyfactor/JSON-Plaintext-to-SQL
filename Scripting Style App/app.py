import sqlite3, os, json, traceback

######## Test Variables ##
json_files_gb = []
parsed_data_gb = []
data_for_db_gb = []
###########################
def db_initializer_fn():
  '''
  Initializes db
  Creates table with necessary columns
  returns cursor, connection

  gets:-
  returns: cursor, connection
  next fn: db_operation_fn
  '''
  connection = sqlite3.connect('main test.db')
  cursor = connection.cursor()
  create_table = ("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY, title text, score int,"
                " retrieved_on int, permalink text, over_18 int,"
                " num_comments int, post_id text,"
                " gilded int, full_link text,"
                " created_utc int, author text, url text)")
  cursor.execute(create_table)
  connection.commit()
  return cursor, connection


def listing_json_files_fn():
  '''
  Gets all the data JSON file
  in the current directory,
  returns them packaged in a list.

  gets:-
  returns: json_files
  next fn: json_to_data_fn
  '''
  json_files = []
  os.chdir("dataset")
  for file in os.listdir():
    json_files.append(file)
  json_files_gb = json_files
  return json_files

def json_to_data_fn(json_file):
  '''
  Reads the files in json_file,
  converts them into a list of dictionary

  gets: json_file
  returns: parsed_data
  next fn: data_for_db_fn
  '''
  parsed_data = []
  with open(json_file, mode='r', encoding='utf-8') as f:
    data = f.read().split('\n')
  for line in data[:-1]:
    # the last line is an empty line
    try:
      parsed_data.append(json.loads(line))
    except Exception:
      print(line)
      traceback.print_exc()
      

  parsed_data_gb = parsed_data
  return parsed_data

def data_for_db_fn(parsed_data):
  '''
  Converts the parsed data
  to a list of tuple
  each tuple contains select data

  gets: parsed_data
  returns: data_for_db
  next fn: db_operation
  '''
  keys_for_db = ['title', 'score', 'retrieved_on',
                 'permalink', 'over_18', 'num_comments',
                 'id', 'gilded', 'full_link', 'created_utc',
                 'author', 'url']
  data_for_db = []
  for data in parsed_data:
    data_for_db.append(tuple([data[key] for key in keys_for_db]))
  data_for_db_gb= data_for_db
  return data_for_db

def db_operation_fn(data_for_db, cursor, connection):
  '''
  Inserts data into db

  gets: data_for_db, cursor, connection
  returns: status
  next fn: -
  '''
  cursor.executemany(
    ("INSERT INTO posts(title, score, retrieved_on, permalink,"
    "over_18, num_comments, post_id, gilded, full_link, created_utc, author, url) "
    "VALUES (?,?,?,?,?,?,?,?,?,?,?)"), data_for_db)
  connection.commit()
  return True

def main():
  cursor, connection= db_initializer_fn()
  json_files= listing_json_files_fn()
  for json_file in json_files:
    parsed_data= json_to_data_fn(json_file)
    data_for_db = data_for_db_fn(parsed_data)
    status = db_operation_fn(data_for_db, cursor, connection)
    if status:
      print(json_file)
  connection.close()

if __name__ == "__main__":
  main()
