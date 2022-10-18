from model.planos import Planos
from conexion.oracle_queries import OracleQueries
from utils.in_out import le_int
import PySimpleGUI as sg

class Controller_Planos:
    def __init__(self):
        pass

    def inserir_plano(self) -> Planos:

        oracle = OracleQueries(can_write=True)
        oracle.connect()
        id_plano = oracle.sqlToDataFrame("select PLANOS_ID_PLANO_SEQ.NEXTVAL id from sys.dual").id.values[0]
        window = sg.Window("Novo Plano",
                            [
                                [sg.T("Nome: "), sg.Input(s=(20, 1), key='-NOME-')],
                                [sg.T("Valor: "), sg.Input(s=(20, 1), key='-VALOR-')],
                                [sg.Col([[sg.B("OK", key='-OK-')]], element_justification="right", expand_x=True)]
                            ])

        valido = False

        while not valido:

            event, values = window.read()

            if event == '-OK-':
                try:
                    nome = values['-NOME-']
                    valor = values['-VALOR-']
                    valido = True
                except ValueError:
                    sg.PopupOK("Valor invalido!")

        window.close()

        oracle.write(
            f"insert into planos values ({id_plano}, '{nome}', '{valor}')")


        df_plano = oracle.sqlToDataFrame(
            f"select id_plano, nome, valor from planos where id_plano = '{id_plano}'")
        novo_plano = Planos(
            df_plano.id_plano.values[0],
            df_plano.nome.values[0],
            df_plano.valor.values[0]
        )
        sg.PopupOK("O seguinte plano foi criado:", novo_plano.to_string())
        return novo_plano

    def atualizar_plano(self) -> Planos:
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        id_plano = le_int("ID do plano que deseja alterar:")

        if not self.verifica_existencia_plano(oracle, id_plano):
            df_plano = oracle.sqlToDataFrame(
                f"select id_plano, nome, valor from planos where id_plano = {id_plano}")

            plano = Planos(
                df_plano.id_plano.values[0],
                df_plano.nome.values[0],
                df_plano.valor.values[0]
            )

            window = sg.Window("Alterar Plano",
                            [
                                [sg.T("Deixe em branco para nao alterar")],
                                [sg.T("Nome: "), sg.Input(s=(20, 1), key='-NOME-')],
                                [sg.T("Valor:  "), sg.Input(s=(20, 1), key='-VALOR-')],
                                [sg.Col([[sg.B("OK", key='-OK-')]], pad=(0, 0), element_justification="right", expand_x=True)]
                            ])

            while True:

                event, values = window.read()

                if event == sg.WINDOW_CLOSED:
                    novo_nome = plano.nome_plano
                    novo_valor = plano.valor_plano
                    break
                if event == '-OK-':
                    try:
                        if values['-VALOR-'] == "":
                            novo_valor = plano.valor_plano
                        else:
                            novo_valor = values['-VALOR-']
                        if values['-NOME-'] == "":
                            novo_nome = plano.nome_plano
                        else:
                            novo_nome = values['-NOME-']
                        window.close()
                        break
                    except ValueError:
                        sg.PopupOK("Valor invalido!")

            oracle.write(
                f"update planos set nome = '{novo_nome}', valor = {novo_valor} where id_plano = {id_plano}")

            df_plano = oracle.sqlToDataFrame(
                f"select id_plano, nome, valor from planos where id_plano = {id_plano}")
            plano_atualizado = Planos(
                df_plano.id_plano.values[0],
                df_plano.nome.values[0],
                df_plano.valor.values[0]
            )
            sg.PopupOK("Plano atualizado:", plano_atualizado.to_string())
            return plano_atualizado
        else:
            sg.PopupOK(f"O plano de ID {id_plano} não existe.")
            return None

    def excluir_plano(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        df_planos = oracle.sqlToDataFrame("select id_plano, nome from planos")
        planos = [f"{id}|{df_planos.nome.values[i]}" for i, id in enumerate(df_planos.id_plano.values)]
        layout = [
            [
                sg.Combo(planos, planos[0], readonly=True, k='-PLANOS-'),
                sg.B("Excluir", k='-EXCLUIR-'),
                sg.B("Cancelar", k='-CANCELAR-')
            ]
        ]

        window = sg.Window("Excluir Plano", layout)

        while True:
            event, values = window.read()
            if event in (sg.WINDOW_CLOSED, '-CANCELAR-'):
                break
            elif event == '-EXCLUIR-':
                delete_id = values['-PLANOS-'].split("|")[0]
                oracle.write(f"delete from socios where id_plano = {delete_id}")
                oracle.write(f"delete from planos where id_plano = {delete_id}")
                df_planos = oracle.sqlToDataFrame("select id_plano, nome from planos")
                planos = [f"{id}|{df_planos.nome.values[i]}" for i, id in enumerate(df_planos.id_plano.values)]
                window['-PLANOS-'].update(values=planos, value=planos[0])
        window.close()

    def verifica_existencia_plano(self, oracle: OracleQueries, id_plano:int = None) -> bool:
        df_plano = oracle.sqlToDataFrame(
            f"select id_plano, nome, valor from planos where id_plano = {id_plano}")
        return df_plano.empty
