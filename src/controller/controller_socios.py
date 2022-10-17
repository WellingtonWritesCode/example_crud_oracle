from model.socios import Socios
from conexion.oracle_queries import OracleQueries
import PySimpleGUI as sg
import re
import datetime as dt
from utils.in_out import le_cpf

class Controller_Socio:
    def __init__(self):
        pass

    def inserir_socio(self) -> Socios:

        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo CPF
        cpf = le_cpf("CPF:")

        if self.verifica_existencia_socio(oracle, cpf):
            # Solicita ao sócio o novo nome
            aux = dt.date.today().strftime("%d/%m/%Y")
            data_associacao = f"to_date({aux}, dd/mm/yyyy)"

            layout_l = [
                [sg.T("Nome:")],
                [sg.T("Endereco:")],
                [sg.T("Telefone:")],
                [sg.T("E-mail:")],
                [sg.T("Id Plano:")]
            ]

            layout_r = [
                [sg.Input(s=(30, 1), k='-NOME-')],
                [sg.Input(s=(30, 1), k='-ENDERECO-')],
                [sg.Input(s=(30, 1), k='-TELEFONE-')],
                [sg.Input(s=(30, 1), k='-EMAIL-')],
                [sg.Col([[sg.Input(s=(5, 1), k='-ID-')]], pad=(0, 0), vertical_alignment="top"),
                sg.Col([[sg.B("OK", k='-OK-')]], element_justification="right", expand_x=True, pad=(0, 0))]
            ]

            layout = [
                [sg.Col(layout_l, pad=(0, 0), vertical_alignment="top"), sg.Col(layout_r, pad=(0, 0), element_justification="right")],
            ]

            window = sg.Window("Inserir Socio", layout)

            while True:
                error = ""

                event, values = window.read()

                if event == sg.WINDOW_CLOSED:
                    break
                if event == '-OK-':
                    nome = values['-NOME-']
                    endereco = values['-ENDERECO-']
                    telefone = values['-TELEFONE-']

                    if not re.match("[a-zA-Z0-9]+@[[a-zA-Z0-9]+\.[a-zA-Z0-9]+", values['-EMAIL-']):
                        valid_email = False
                        error += "Email invalido!\n"
                    else:
                        valid_email = True
                        email = values['-EMAIL-']
                    try:
                        id_plano = int(values['-ID-'])
                        valid_int = True
                    except ValueError:
                        valid_int = False
                        error += "ID Invalido!\n"
                    if not valid_email or not valid_int:
                        sg.PopupOK(error[:-2])
                    else:
                        break

            window.close()
            # Insere e persiste o novo cliente
            oracle.write(
                f"insert into socios values ('{cpf}', {id_plano}, '{nome}', '{endereco}', '{data_associacao}', NULL, '{telefone}', '{email}')")
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_socio = oracle.sqlToDataFrame(
                f"select cpf, id_plano, endereco, nome, data_associacao, data_desativacao, telefone, email from socios where cpf = '{cpf}'")
            # Cria um novo objeto Cliente
            novo_socio = Socios(
                df_socio.cpf.values[0],
                df_socio.id_plano.values[0],
                df_socio.endereco.values[0],
                df_socio.nome.values[0],
                df_socio.data_associacao.values[0],
                df_socio.data_desativacao.values[0],
                df_socio.telefone.values[0],
                df_socio.email.values[0]
            )
            # Exibe os atributos do novo cliente
            sg.PopupOK("O seguinte socio foi cadastrado", novo_socio.to_string())
            # Retorna o objeto novo_cliente para utilização posterior, caso necessário
            return novo_socio
        else:
            sg.PopupOK("CPF ja cadastrado")
            return None

    def atualizar_socio(self) -> Socios:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        cpf = le_cpf("CPF:")

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
                df_socio.id_plano.values[0],
                df_socio.endereco.values[0],
                df_socio.nome.values[0],
                df_socio.data_associacao.values[0],
                df_socio.data_desativacao.values[0],
                df_socio.telefone.values[0],
                df_socio.email.values[0]
            )
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
        cpf = le_cpf("CPF:")

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
                df_socio.id_plano.values[0],
                df_socio.endereco.values[0],
                df_socio.nome.values[0],
                df_socio.data_associacao.values[0],
                df_socio.data_desativacao.values[0],
                df_socio.telefone.values[0],
                df_socio.email.values[0]
            )
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
