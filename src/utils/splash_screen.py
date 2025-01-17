from conexion.oracle_queries import OracleQueries
import PySimpleGUI as sg

QUERY_COUNT = 'select count(1) as total_{tabela} from {tabela}'

class SplashScreen:

    def __init__(self):
        self.qry_total_socios = QUERY_COUNT.format(tabela="socios")
        self.qry_total_planos = QUERY_COUNT.format(tabela="planos")
        self.qry_total_mensalidades = QUERY_COUNT.format(tabela="mensalidades")

    def get_total_socios(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_socios)["total_socios"].values[0]

    def get_total_planos(self):
        oracle = OracleQueries()
        oracle.connect()
        return oracle.sqlToDataFrame(self.qry_total_planos)["total_planos"].values[0]

    def get_updated_screen(self):

        layout_l = [[sg.T("1- Socios:")],
                    [sg.T("2- Planos:")]]

        layout_r = [[sg.T(self.get_total_socios(), key='-SOCIOS-')],
                    [sg.T(self.get_total_planos(), key='-PLANOS-')]]

        nomes = [[sg.T("Cleverton dos Santos Liltk")],
                [sg.T("Gustavo de Oliveira Christ")],
                [sg.T("Jhony Rodrigues de Souza")],
                [sg.T("Lucio Ewald do Nascimento")],
                [sg.T("Wellington da Silva Barbosa Junior")]]

        layout = [[sg.Col([[sg.T("Sistema de controle de socios torcedores do SC Brasil")]], element_justification='center', pad=(0,0), expand_x=True)],
                [sg.T("Total de registros existentes:")],
                [sg.Col(layout_l, pad=(0, 0)), sg.Col(layout_r, element_justification='right', pad=(0, 0), expand_x=True)],
                [sg.T()],
                [sg.Col([[sg.T("Criado por: ")]], vertical_alignment='top', pad=(0,0)), sg.Col(nomes, vertical_alignment='top', pad=(0,0))],
                [sg.T()],
                [sg.Col([[sg.T("Disciplina: ")]], vertical_alignment='top', pad=(0,0)), sg.Col([[sg.T("Banco de Dados")],
                                                                                                [sg.T("2022/2")]], vertical_alignment='top', pad=(0,0))],
                [sg.T("Professor: Prof. M.Sc. Howard Roatti")],
                [sg.Col([[sg.B("Ok")]], element_justification='center', pad=(0,0), expand_x=True)]]

        sg.Window("", layout, finalize=True).read(close=True)