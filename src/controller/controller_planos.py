from model.planos import Planos
from conexion.oracle_queries import OracleQueries


class Controller_Planos:
    def __init__(self):
        pass

    def inserir_plano(self) -> Planos:

        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo id do plano
        id_plano = input("Plano (Novo): ")

        if self.verifica_existencia_socio(oracle, id_plano):

            # Solicita novo plano
            nome_plano = input("Nome plano (Novo): ")
            valor_plano = input("Valor plano (Novo): ")


            # Insere e persiste o novo plano
            oracle.write(
                f"insert into planos values ('{nome_plano}', '{valor_plano}')")


            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_plano = oracle.sqlToDataFrame(
                f"select nome, valor from planos where id_plano = '{id_plano}'")
            # Cria um novo objeto Cliente
            novo_plano = Planos(
                df_plano.nome.values[0],
                df_plano.valor.values[0],
            )
            # Exibe os atributos do novo cliente
            print(novo_plano.to_string())
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_plano
        else:
            print(f"O Plano de ID {id_plano} já está cadastrado.")
            return None
            
    def atualizar_plano(self) -> Planos:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        id_plano = int(input("ID so plano que deseja alter o nome: "))

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_plano(oracle, id_plano):
            # Solicita a nova descrição do cliente
            novo_nome = input("Nome (Novo): ")
            # Atualiza o nome do plano existente
            oracle.write(
                f"update planos set nome = '{novo_nome}' where id_plano = {id_plano}")
            # Recupera os dados do novo plano criado transformando em um DataFrame

            df_plano = oracle.sqlToDataFrame(
                f"select id_plano, nome from planos where id_plano = {id_plano}")
            # Cria um novo objeto cliente
            plano_atualizado = Planos(
                df_plano.id_plano.values[0],
                df_plano.id_plano.values[0],

            # Exibe os atributos do novo cliente
            print(plano_atualizado.to_string())
            # Retorna o objeto plano_atualizado para utilização posterior, caso necessário
            return plano_atualizado
        else:
            print(f"O ID {id_plano} não existe.")
            return None

    def excluir_plano(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o ID do Plano a ser excluido
        id_plano = int(input("ID do plano que irá ser excluido: "))

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_plano(oracle, id_plano):
            # Recupera os dados do plano e transforma em um DataFrame
            df_plano = oracle.sqlToDataFrame(
                f"select id_plano, nome from planos where id_plano = {id_plano}")
            # Revome o plano da tabela
            oracle.write(f"delete from planos where id_plano = {id_plano}")
            # Cria um novo objeto Cliente para informar que foi removido
            plano_excluido = Planos(
                df_plano.id_plano.values[0],
                df_socio.nome.values[0]
            # Exibe os atributos do plano excluído
            print("Plano Removido com Sucesso!")
            print(plano_excluido.to_string())
        else:
            print(f"O plano de ID {id_plano} não existe.")

    def verifica_existencia_plano(self, oracle: OracleQueries, id_plano: double = None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_plano = oracle.sqlToDataFrame(
            f"select id_plano, nome from planos where id_plano = {id_plano}")
        return df_plano.empty
