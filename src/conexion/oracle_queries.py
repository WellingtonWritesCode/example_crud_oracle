###########################################################################
# Author: Howard Roatti
# Created: 02/09/2022
# Last Update: 03/09/2022
#
# Essa classe auxilia na conexão com o Banco de Dados Oracle
# Documentação base:
#                  (1) https://cx-oracle.readthedocs.io/en/latest/user_guide/sql_execution.html
#                  (2) https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html
#                  (3) https://cx-oracle.readthedocs.io/en/latest/index.html
###########################################################################

import json
import cx_Oracle
from pandas import DataFrame

class OracleQueries:

    def __init__(self, can_write:bool=False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = 'XEPDB1'
        self.sid = 'XE'
        self.cur = False

    def __del__(self):
        if self.cur:
            self.close()

    def connectionString(self, in_container:bool=False):

        if not in_container:
            string_connection = cx_Oracle.makedsn(host=self.host,
                                                port=self.port,
                                                sid=self.sid
                                                )
        elif in_container:
            string_connection = cx_Oracle.makedsn(host=self.host,
                                                port=self.port,
                                                service_name=self.service_name
                                                )
        return string_connection

    def connect(self):

        self.conn = cx_Oracle.connect("labdatabase/labDatabase2022@localhost:1521/XEPDB1")
        self.cur = self.conn.cursor()
        return self.cur

    def sqlToDataFrame(self, query:str) -> DataFrame:

        self.cur.execute(query)
        rows = self.cur.fetchall()
        return DataFrame(rows, columns=[col[0].lower() for col in self.cur.description])

    def sqlToMatrix(self, query:str) -> tuple:

        self.cur.execute(query)
        rows = self.cur.fetchall()
        matrix = [list(row) for row in rows]
        columns = [col[0].lower() for col in self.cur.description]
        return matrix, columns

    def sqlToJson(self, query:str):

        self.cur.execute(query)
        columns = [col[0].lower() for col in self.cur.description]
        self.cur.rowfactory = lambda *args: dict(zip(columns, args))
        rows = self.cur.fetchall()
        return json.dumps(rows, default=str)

    def write(self, query:str):
        if not self.can_write:
            raise Exception('Can\'t write using this connection')

        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()

    def executeDDL(self, query:str):

        self.cur.execute(query)