from model.socios import Socios
from conexion.oracle_queries import OracleQueries
import PySimpleGUI as sg
import re
import datetime as dt
from utils.in_out import le_cpf
from utils.general_utils import capitalize_name

class Controller_Socios:
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
            data_associacao = f"to_date('{aux}', 'dd/mm/yyyy')"

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
                        sg.PopupOK(error[:-1])
                    else:
                        break

            window.close()
            # Insere e persiste o novo cliente
            oracle.write(
                f"insert into socios values ('{cpf}', {id_plano}, '{nome}', '{endereco}', {data_associacao}, NULL, '{telefone}', '{email}')")
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
        cpf = le_cpf("CPF do socio que deseja alterar:")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_socio(oracle, cpf):
            # Solicita a nova descrição do cliente
            df_socio = oracle.sqlToDataFrame(
                f"select cpf, id_plano, endereco, nome, data_associacao, data_desativacao, telefone, email from socios where cpf = '{cpf}'")

            layout_l = [
                [sg.T("Nome:")],
                [sg.T("Endereco:")],
                [sg.T("Telefone:")],
                [sg.T("E-mail:")]
            ]

            layout_r = [
                [sg.Input(s=(30, 1), k='-NOME-')],
                [sg.Input(s=(30, 1), k='-ENDERECO-')],
                [sg.Input(s=(30, 1), k='-TELEFONE-')],
                [sg.Input(s=(30, 1), k='-EMAIL-')]
            ]

            layout_IDl = [
                [sg.T("Id Plano:")]
            ]

            layout_IDr = [
                [
                    sg.Col([[sg.Input(s=(5, 1), k='-ID-')]], pad=(0, 0), vertical_alignment="top"),
                    sg.Col([[sg.B("OK", k='-OK-')]], element_justification="right", expand_x=True, pad=(0, 0))
                ]
            ]

            layout = [
                [sg.T("Deixe em branco para manter o valor atual")],
                [sg.Col(layout_l, pad=(0, 0)), sg.Col(layout_r, pad=(0, 0), element_justification="right")],
                [sg.T("Data Desativacao(DD/MM/AAAA):"), sg.Input(s=(10, 1), k='-DATA-')],
                [sg.Col(layout_IDl, pad=(0, 0), vertical_alignment="top"), sg.Col(layout_IDr, expand_x=True, pad=(0, 0), element_justification="right")]
            ]

            window = sg.Window("Atualizar Socio", layout)

            while True:
                error = ""

                event, values = window.read()

                if event == sg.WINDOW_CLOSED:
                    break
                if event == '-OK-':
                    if re.match("[0-9]{2}/[0-9]{2}/[0-9]{4}", values['-DATA-']):
                        try:
                            data_arr = values['-DATA-'].split("/")
                            nova_data = dt.datetime(int(data_arr[2]), int(data_arr[1]), int(data_arr[0])).strftime("%d/%m/%Y")
                            valid_date = True
                        except ValueError:
                            valid_date = False
                    elif values['-DATA-'] == "":
                        valid_date = True
                    else:
                        valid_date = False
                    if not valid_date:
                        error += "Data Invalida!\n"
                    if values['-NOME-'] != "":
                        novo_nome = values['-NOME-']
                    else:
                        novo_nome = df_socio.nome.values[0]
                    if values['-ENDERECO-'] != "":
                        novo_endereco = values['-ENDERECO-']
                    else:
                        novo_endereco = df_socio.endereco.values[0]
                    if values['-TELEFONE-'] != "":
                        novo_telefone = values['-TELEFONE-']
                    else:
                        novo_telefone = df_socio.telefone.values[0]

                    if values['-EMAIL-'] != "":
                        if not re.match("[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+", values['-EMAIL-']):
                            valid_email = False
                            error += "Email Invalido!\n"
                        else:
                            valid_email = True
                            novo_email = values['-EMAIL-']
                    else:
                        novo_email = df_socio.email.values[0]
                        valid_email = True

                    try:
                        if values['-ID-'] != "":
                            novo_id_plano = int(values['-ID-'])
                        else:
                            novo_id_plano = df_socio.id_plano.values[0]
                        valid_int = True
                    except ValueError:
                        valid_int = False
                        error += "ID Invalido!\n"
                    if not valid_email or not valid_int or not valid_date:
                        sg.PopupOK(error[:-1])
                    else:
                        break

            window.close()
            # Atualiza o nome do cliente existente
            update = (
                f"update socios set nome = '{novo_nome}', "+
                f"endereco = '{novo_endereco}', "+
                f"telefone = '{novo_telefone}', "+
                f"email = '{novo_email}', "+
                f"id_plano = {novo_id_plano} "+
                f"where cpf = '{cpf}'"
            )
            oracle.write(update)
            if nova_data != "":
                oracle.write(
                    f"update socios set data_desativacao = to_date('{nova_data}', 'dd/mm/yyyy') where cpf = '{cpf}'"
                )
            # Recupera os dados do novo cliente criado transformando em um DataFrame
            df_socio_atualizado = oracle.sqlToDataFrame(
                f"select cpf, id_plano, endereco, nome, data_associacao, data_desativacao, telefone, email from socios where cpf = '{cpf}'")
            # Cria um novo objeto cliente
            socio_atualizado = Socios(
                df_socio_atualizado.cpf.values[0],
                df_socio_atualizado.id_plano.values[0],
                df_socio_atualizado.endereco.values[0],
                df_socio_atualizado.nome.values[0],
                df_socio_atualizado.data_associacao.values[0],
                df_socio_atualizado.data_desativacao.values[0],
                df_socio_atualizado.telefone.values[0],
                df_socio_atualizado.email.values[0]
            )
            # Exibe os atributos do novo cliente
            sg.PopupOK("Socio atualizado:", socio_atualizado.to_string())
            # Retorna o objeto cliente_atualizado para utilização posterior, caso necessário
            return socio_atualizado
        else:
            sg.PopupOK(f"O CPF {cpf} não existe.")
            return None

    def excluir_socio(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_socio = oracle.sqlToDataFrame(
            f"select cpf, nome from socios")
        
        socios = [f"{capitalize_name(nome)}|{df_socio.cpf.values[i]}" for i, nome in enumerate(df_socio.nome.values)]

        layout = [[sg.Combo(socios, k='-SOCIOS-', default_value=socios[0], readonly=True), sg.B("Excluir", k='-EXCLUIR-'), sg.B("Cancelar", k='-CANCELAR-')]]
        window = sg.Window("Excluir", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, '-CANCELAR-'):
                break
            elif event == '-EXCLUIR-':
                print(values['-SOCIOS-'])
                delete_cpf = values['-SOCIOS-'].split("|")[1]
                oracle.write(f"delete from mensalidades where cpf = '{delete_cpf}'")
                oracle.write(f"delete from socios where cpf = '{delete_cpf}'")
                df_socio = oracle.sqlToDataFrame(
                     f"select cpf, nome from socios")
                socios = [f"{capitalize_name(nome)}|{df_socio.cpf.values[i]}" for i, nome in enumerate(df_socio.nome.values)]
                window['-SOCIOS-'].update(values=socios, default_value=socios[0])

        window.close()

    def verifica_existencia_socio(self, oracle: OracleQueries, cpf: str = None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_socio = oracle.sqlToDataFrame(
            f"select cpf, nome from socios where cpf = '{cpf}'")
        return df_socio.empty
