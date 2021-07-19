from json_data import JsonToDataCLS
from dataop import DatabaseInterface


def main():
  dataop = DatabaseInterface()
  json_data_cls =  JsonToDataCLS()

  json_files= json_data_cls.listing_json_files_fn()
  dataop.initialize_table()

  for json_file in json_files:
    parsed_data= json_data_cls.json_to_data_fn(json_file)
    data_for_db= json_data_cls.data_for_db_fn(parsed_data)
    status = dataop.db_operation_fn(data_for_db)
    if status:
      print(json_file)
  dataop.close_connection()


if __name__ == "__main__":
  main()