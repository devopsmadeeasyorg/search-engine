"""
Database search module
"""
import os
import json
import configparser
import datetime
import mysql.connector

class DBSearch():
    """
    Class to interact with Database API
    """
    _db_con = None
    _db_session = None
    def __init__(self) -> None:
        super().__init__()
        self.host, self.tables = self.__parse_config()

    def connect(self):
        if DBSearch._db_con == None:
            DBSearch._db_con = mysql.connector.connect(
                host="localhost",
                user="krishna",
                password="Krishna@123",
                database="csit"
            )
        if DBSearch._db_session == None:
            DBSearch._db_session = DBSearch._db_con.cursor()
        return DBSearch._db_session
    
    def close(self):
        if DBSearch._db_session:
            DBSearch._db_session.close()
        if DBSearch._db_con:
            DBSearch._db_con.close()

    def __parse_config(self):
        """
        Method to parse config file
        """
        CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'data_sources.config')
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        return config["DB"]["server"], config["DB"]["tables"].split(',')
    
    def search(self, search_list=[]):
        """
        Method to search in DB
        Args: search_list(list, optional)
        """
        try:
            db_result = []
            for table in self.tables:
                table_columns = []
                table_data = []
                table_complete_data = {}
                query = f"help table {table};"
                db_con = DBSearch().connect()
                columns = db_con.execute(query).fetchall()
                for column in columns:
                    if column[1].strip() == 'CV':
                        table_columns.append(column[0].strip())
                query = f"lock row for access sel top 5 * from {table}"
                if search_list:
                    list_operand = "".join(f"{str(search_token)}%" for search_token in search_list)
                    search_query_str = " OR ".join(f"{str(item)} LIKE '%{list_operand}'" for item in table_columns)
                    query += f" where {search_query_str}"
                print(query)
                rows = self.connect().execute(query).fetchall()
                for row in rows:
                    row_dict = dict(zip(table_columns, row))
                    table_data.append(row_dict)
                for data in table_data:
                    for key, value in data.items():
                        if type(value) is datetime.datetime:
                            data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                table_complete_data['table'] = table
                table_complete_data['data'] = table_data
                db_result.append(table_complete_data)
            return json.dumps(db_result, indent=' ')
        except Exception as e:
            print(e)


    