import json, os, traceback

class JsonToDataCLS:
  '''
  Returns a list of tuple for db
  from a hardcoded directory path of 
  individual json like files
  '''
  def __init__(self):
    # hardcoded path to the directory in the working directory
    self.data_dir = "dataset"
    # extracting keys from data
    self.keys_for_db = ['title', 'score', 'retrieved_on',
                        'permalink', 'over_18', 'num_comments',
                        'id', 'gilded', 'full_link', 'created_utc',
                        'author', 'url']
  

  def listing_json_files_fn(self):
    '''
    Gets all the data JSON file
    in the current directory,
    returns them packaged in a list.

    gets:-
    returns: json_files
    next fn: json_to_data_fn
    '''
    json_files = []
    os.chdir(self.data_dir)
    for file in os.listdir():
      json_files.append(file)

    return json_files

  def json_to_data_fn(self, json_file):
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
      # Temporary code to check and traceback errors
      try:
        parsed_data.append(json.loads(line))
      except Exception:
        print(line)
        traceback.print_exc()
        
    return parsed_data

  def data_for_db_fn(self,parsed_data):
    '''
    Converts the parsed data
    to a list of tuple
    each tuple contains select data

    gets: parsed_data
    returns: data_for_db
    next fn: db_operation module
    '''
    data_for_db = []
    for data in parsed_data:
      # example [(), (),  ...]
      # contains only values from the dictionary
      data_for_db.append(tuple([data[key] for key in self.keys_for_db]))

    return data_for_db