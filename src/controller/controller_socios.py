from model.socios import Socios
from conexion.oracle_queries import OracleQueries


class Controller_Socio:
    def __init__(self):
        pass

    def inserir_socio(self) -> Socios:

        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CPF
        cpf = input("CPF (Novo): ")

        if self.verifica_existencia_socio(oracle, cpf):
            # Solicita ao sócio o novo nome
            nome = input("Nome (Novo): ")
            endereco = input("Enderecço (Novo): ")
            data_associacao = input("Data de associação (Novo): ")
            data_desativacao = input("Data de desativação (Novo): ")
            telefone = input("Telefone (Novo): ")
            email = input("Email (Novo): ")
            # Insere e persiste o novo cliente
            oracle.write(
                f"insert into socios values ('{cpf}', '{nome}', '{endereco}', '{data_associacao}', '{data_desativacao}', '{telefone}', '{email}')")
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_socio = oracle.sqlToDataFrame(
                f"select cpf, nome from socios where cpf = '{cpf}'")
            # Cria um novo objeto Cliente
            novo_socio = Socios(
                df_socio.cpf.values[0],
                df_socio.nome.values[0],
                df_socio.endereco.values[0],
                df_socio.data_associacao.values[0],
                df_socio.data_desativacao.values[0],
                df_socio.telefone.values[0],
                df_socio.email.values[0]
            )
            # Exibe os atributos do novo cliente
            print(novo_socio.to_string())
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_socio
        else:
            print(f"O CPF {cpf} já está cadastrado.")
            return None

    def atualizar_socio(self) -> Socios:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = int(input("CPF do socio que deseja alterar o nome: "))

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_socio(oracle, cpf):
            # Solicita a nova descrição do cliente
            novo_nome = input("Nome (Novo): ")
            # Atualiza o nome do cliente existente
            oracle.write(
                f"update socios set nome = '{novo_nome}' where cpf = {cpf}")
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_socio = oracle.sqlToDataFrame(
                f"select cpf, nome from socios where cpf = {cpf}")
            # Cria um novo objeto cliente
            socio_atualizado = Socios(
                df_socio.cpf.values[0],
                df_socio.nome.values[0],
                df_socio.endereco.values[0],
                df_socio.data_associacao.values[0],
                df_socio.data_desativacao.values[0],
                df_socio.telefone.values[0],
                df_socio.email.values[0])
            # Exibe os atributos do novo cliente
            print(socio_atualizado.to_string())
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return socio_atualizado
        else:
            print(f"O CPF {cpf} não existe.")
            return None

    def excluir_socio(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o CPF do Cliente a ser alterado
        cpf = int(input("CPF do Sócio que irá excluir: "))

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_cliente(oracle, cpf):
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_socio = oracle.sqlToDataFrame(
                f"select cpf, nome from socios where cpf = {cpf}")
            # Revome o cliente da tabela
            oracle.write(f"delete from socios where cpf = {cpf}")
            # Cria um novo objeto Cliente para informar que foi removido
            socio_excluido = Socios(
                df_socio.cpf.values[0],
                df_socio.nome.values[0],
                df_socio.endereco.values[0],
                df_socio.data_associacao.values[0],
                df_socio.data_desativacao.values[0],
                df_socio.telefone.values[0],
                df_socio.email.values[0])
            # Exibe os atributos do cliente excluído
            print("Sócio Removido com Sucesso!")
            print(socio_excluido.to_string())
        else:
            print(f"O CPF {cpf} não existe.")

    def verifica_existencia_socio(self, oracle: OracleQueries, cpf: str = None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_socio = oracle.sqlToDataFrame(
            f"select cpf, nome from socios where cpf = {cpf}")
        return df_socio.empty
