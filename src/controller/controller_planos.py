from model.planos import Planos
from conexion.oracle_queries import OracleQueries
from utils.in_out import le_int
import PySimpleGUI as sg

class Controller_Planos:
    def __init__(self):
        pass

    def inserir_plano(self) -> Planos:

        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuario o novo id do plano
        id_plano = oracle.sqlToDataFrame("select PLANOS_ID_PLANO_SEQ.NEXTVAL id from sys.dual").id.values[0]

        # Solicita novo plano
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

        # Insere e persiste o novo plano
        oracle.write(
            f"insert into planos values ({id_plano}, '{nome}', '{valor}')")


        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_plano = oracle.sqlToDataFrame(
            f"select id_plano, nome, valor from planos where id_plano = '{id_plano}'")
        # Cria um novo objeto Cliente
        novo_plano = Planos(
            df_plano.id_plano.values[0],
            df_plano.nome.values[0],
            df_plano.valor.values[0]
        )
        # Exibe os atributos do novo cliente
        sg.PopupOK("O seguinte plano foi criado:", novo_plano.to_string())
        # Retorna o objeto novo_cliente para utilização posterior, caso necessário
        return novo_plano

    def atualizar_plano(self) -> Planos:
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o código do cliente a ser alterado
        id_plano = le_int("ID do plano que deseja alterar:")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_plano(oracle, id_plano):
            # Solicita a nova descrição do cliente
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

            # Atualiza o nome do plano existente
            oracle.write(
                f"update planos set nome = '{novo_nome}', valor = {novo_valor} where id_plano = {id_plano}")
            # Recupera os dados do novo plano criado transformando em um DataFrame

            df_plano = oracle.sqlToDataFrame(
                f"select id_plano, nome, valor from planos where id_plano = {id_plano}")
            # Cria um novo objeto cliente
            plano_atualizado = Planos(
                df_plano.id_plano.values[0],
                df_plano.nome.values[0],
                df_plano.valor.values[0]
            )
            # Exibe os atributos do novo cliente
            sg.PopupOK("Plano atualizado:", plano_atualizado.to_string())
            # Retorna o objeto plano_atualizado para utilização posterior, caso necessário
            return plano_atualizado
        else:
            sg.PopupOK(f"O plano de ID {id_plano} não existe.")
            return None

    def excluir_plano(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        # Solicita ao usuário o ID do Plano a ser excluido
        id_plano = id_plano = le_int("ID do plano que deseja excluir:")

        # Verifica se o cliente existe na base de dados
        if not self.verifica_existencia_plano(oracle, id_plano):
            # Recupera os dados do plano e transforma em um DataFrame
            df_plano = oracle.sqlToDataFrame(
                f"select id_plano, nome, valor from planos where id_plano = {id_plano}")
            # Revome o plano da tabela
            oracle.write(f"delete from planos where id_plano = {id_plano}")
            # Cria um novo objeto Cliente para informar que foi removido
            plano_excluido = Planos(
                df_plano.id_plano.values[0],
                df_plano.nome.values[0],
                df_plano.valor.values[0]
            )
            # Exibe os atributos do plano excluído
            sg.PopupOK("Plano excluido com sucesso!", "Plano excluido:", plano_excluido.to_string())
        else:
            sg.PopupOK(f"O plano de ID {id_plano} não existe.")

    def verifica_existencia_plano(self, oracle: OracleQueries, id_plano:int = None) -> bool:
        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_plano = oracle.sqlToDataFrame(
            f"select id_plano, nome, valor from planos where id_plano = {id_plano}")
        return df_plano.empty
