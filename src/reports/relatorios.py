from pandas import DataFrame
from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        with open("src/sql/relatorio_socios.sql") as f:
            self.query_relatorio_socios = f.read()

        with open("src/sql/relatorio_planos.sql") as f:
            self.query_relatorio_planos = f.read()

        with open("src/sql/relatorio_socios_por_plano.sql") as f:
            self.query_relatorio_socios_por_plano = f.read()

    def get_relatorio_socios(self) -> DataFrame:
        oracle = OracleQueries()
        oracle.connect()

        return oracle.sqlToDataFrame(self.query_relatorio_socios)

    def get_relatorio_planos(self) -> DataFrame:
        oracle = OracleQueries()
        oracle.connect()

        return oracle.sqlToDataFrame(self.query_relatorio_planos)

    def get_relatorio_socios_por_plano(self) -> DataFrame:
        oracle = OracleQueries()
        oracle.connect()

        return oracle.sqlToDataFrame(self.query_relatorio_socios_por_plano)