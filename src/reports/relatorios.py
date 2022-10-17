from pandas import DataFrame
from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        with open("src/sql/relatorio_socios.sql") as f:
            self.query_relatorio_socios = f.read()

        with open("src/sql/relatorio_planos.sql") as f:
            self.query_relatorio_planos = f.read()

        with open("src/sql/relatorio_mensalidades.sql") as f:
            self.query_relatorio_mensalidades = f.read()

        with open("src/sql/relatorio_socios_por_plano.sql") as f:
            self.query_relatorio_socios_por_plano = f.read()

        with open("src/sql/relatorio_pagamentos_antes_vencimento.sql") as f:
            self.query_relatorio_pagamento_antes_vencimento = f.read()

    def get_relatorio_socios(self) -> DataFrame:
        oracle = OracleQueries()
        oracle.connect()

        return oracle.sqlToDataFrame(self.query_relatorio_socios)

    def get_relatorio_planos(self) -> DataFrame:
        oracle = OracleQueries()
        oracle.connect()

        return oracle.sqlToDataFrame(self.query_relatorio_planos)

    def get_relatorio_mensalidades(self) -> DataFrame:
        oracle = OracleQueries()
        oracle.connect()

        return oracle.sqlToDataFrame(self.query_relatorio_mensalidades)

    def get_relatorio_socios_por_plano(self) -> DataFrame:
        oracle = OracleQueries()
        oracle.connect()

        return oracle.sqlToDataFrame(self.query_relatorio_socios_por_plano)

    def get_relatorio_pagamentos_antes_vencimento(self) -> DataFrame:
        oracle = OracleQueries()
        oracle.connect()

        return oracle.sqlToDataFrame(self.query_relatorio_pagamento_antes_vencimento)