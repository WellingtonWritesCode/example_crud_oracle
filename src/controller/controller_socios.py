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

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        cpf = le_cpf("CPF:")
        if cpf == None:
            return

        if self.verifica_existencia_socio(oracle, cpf):
            aux = dt.date.today().strftime("%d/%m/%Y")
            data_associacao = f"to_date('{aux}', 'dd/mm/yyyy')"

            df_planos = oracle.sqlToDataFrame("select id_plano, nome from planos")
            planos = [f"{id}|{capitalize_name(df_planos.nome.values[i])}" for i, id in enumerate(df_planos.id_plano.values)]

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
                [sg.Col([[sg.Combo(planos, planos[0], k='-ID-', readonly=True)]], pad=(0, 0), vertical_alignment="top"),
                sg.Col([[sg.B("Cancelar", k='-CANCELAR-'), sg.B("OK", k='-OK-')]], element_justification="right", expand_x=True, pad=(0, 0))]
            ]

            layout = [
                [sg.Col(layout_l, pad=(0, 0), vertical_alignment="top"), sg.Col(layout_r, pad=(0, 0), element_justification="right")],
            ]

            window = sg.Window("Inserir Socio", layout)

            email = ""

            while True:

                event, values = window.read()

                if event in (sg.WINDOW_CLOSED, '-CANCELAR-'):
                    break
                elif event == '-OK-':
                    nome = values['-NOME-']
                    endereco = values['-ENDERECO-']
                    telefone = values['-TELEFONE-']
                    id_plano = int(values['-ID-'].split("|")[0])

                    if not re.fullmatch("[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+", values['-EMAIL-']):
                        sg.PopupOK("Email invalido!")
                    else:
                        email = values['-EMAIL-']
                        break

            window.close()

            if email == "":
                return

            oracle.write(
                f"insert into socios values ('{cpf}', {id_plano}, '{nome}', '{endereco}', {data_associacao}, NULL, '{telefone}', '{email}')")

            df_socio = oracle.sqlToDataFrame(
                f"select cpf, id_plano, endereco, nome, data_associacao, data_desativacao, telefone, email from socios where cpf = '{cpf}'")
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
            sg.PopupOK("O seguinte socio foi cadastrado", novo_socio.to_string())
            return novo_socio
        else:
            sg.PopupOK("CPF ja cadastrado")
            return None

    def atualizar_socio(self) -> Socios:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        df_socios = oracle.sqlToDataFrame("select cpf, nome from socios")
        socios = [f"{cpf}|{capitalize_name(df_socios.nome.values[i])}" for i, cpf in enumerate(df_socios.cpf.values)]
        layout = [
            [sg.Combo(socios, socios[0], readonly=True, k='-CPF-'), sg.B("OK", k='-OK-')]
        ]
        cpf = sg.Window("Selecionar Socio", layout).read(close=True)[1]['-CPF-'].split("|")[0]

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
        df_planos = oracle.sqlToDataFrame("select id_plano, nome from planos")
        default_id = oracle.sqlToDataFrame(f"select id_plano from socios where cpf = '{cpf}'").id_plano.values[0]
        default_nome = oracle.sqlToDataFrame(f"select nome from planos where id_plano = {default_id}").nome.values[0]
        planos = [f"{id}|{capitalize_name(df_planos.nome.values[i])}" for i, id in enumerate(df_planos.id_plano.values)]
        layout_IDr = [
            [
                sg.Col([[sg.Combo(planos, f"{default_id}|{capitalize_name(default_nome)}", k='-ID-', readonly=True)]], pad=(0, 0), vertical_alignment="top"),
                sg.Col([[sg.B("Cancelar", k='-CANCELAR-'), sg.B("OK", k='-OK-')]], element_justification="right", expand_x=True, pad=(0, 0))
            ]
        ]

        layout = [
            [sg.T("Deixe em branco para manter o valor atual")],
            [sg.Col(layout_l, pad=(0, 0)), sg.Col(layout_r, pad=(0, 0), element_justification="right")],
            [sg.T("Data Desativacao(DD/MM/AAAA):"), sg.Input(s=(10, 1), k='-DATA-')],
            [sg.Col(layout_IDl, pad=(0, 0), vertical_alignment="top"), sg.Col(layout_IDr, expand_x=True, pad=(0, 0), element_justification="right")]
        ]

        window = sg.Window("Atualizar Socio", layout)
        valid_date = False

        while True:
            error = ""

            event, values = window.read()

            if event in (sg.WINDOW_CLOSED, '-CANCELAR-'):
                break
            if event == '-OK-':
                novo_id_plano = int(values['-ID-'].split("|")[0])
                if re.fullmatch("[0-9]{2}/[0-9]{2}/[0-9]{4}", values['-DATA-']):
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
                    if not re.fullmatch("[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+", values['-EMAIL-']):
                        valid_email = False
                        error += "Email Invalido!\n"
                    else:
                        valid_email = True
                        novo_email = values['-EMAIL-']
                else:
                    novo_email = df_socio.email.values[0]
                    valid_email = True

                if not valid_email or not valid_date:
                    sg.PopupOK(error[:-1])
                else:
                    break

        window.close()
        if not valid_date:
            return

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
        df_socio_atualizado = oracle.sqlToDataFrame(
            f"select cpf, id_plano, endereco, nome, data_associacao, data_desativacao, telefone, email from socios where cpf = '{cpf}'")
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
        sg.PopupOK("Socio atualizado:", socio_atualizado.to_string())
        return socio_atualizado

    def excluir_socio(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_socio = oracle.sqlToDataFrame("select cpf, nome from socios")

        socios = [f"{capitalize_name(nome)}|{df_socio.cpf.values[i]}" for i, nome in enumerate(df_socio.nome.values)]

        layout = [[sg.Combo(socios, k='-SOCIOS-', default_value=socios[0], readonly=True), sg.B("Excluir", k='-EXCLUIR-'), sg.B("Cancelar", k='-CANCELAR-')]]
        window = sg.Window("Excluir Socio", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, '-CANCELAR-'):
                break
            elif event == '-EXCLUIR-':
                delete_cpf = values['-SOCIOS-'].split("|")[1]
                oracle.write(f"delete from socios where cpf = '{delete_cpf}'")
                df_socio = oracle.sqlToDataFrame(
                     f"select cpf, nome from socios")
                socios = [f"{capitalize_name(nome)}|{df_socio.cpf.values[i]}" for i, nome in enumerate(df_socio.nome.values)]
                window['-SOCIOS-'].update(values=socios, value=socios[0])

        window.close()

    def verifica_existencia_socio(self, oracle: OracleQueries, cpf: str = None) -> bool:
        df_socio = oracle.sqlToDataFrame(
            f"select cpf, nome from socios where cpf = '{cpf}'")
        return df_socio.empty
