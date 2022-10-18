import PySimpleGUI as sg
import pandas as pd
from utils.splash_screen import SplashScreen
from utils.general_utils import capitalize_name
from reports.relatorios import Relatorio
from controller.controller_socios import Controller_Socios
from controller.controller_planos import Controller_Planos

tela_inicial = SplashScreen()
relatorios = Relatorio()
ctrl_socios = Controller_Socios()
ctrl_planos = Controller_Planos()

def relatorio_socios() -> None:
    df_socios = relatorios.get_relatorio_socios()

    aux = ""
    tam = len(df_socios.nome.values)-1

    for i, n in enumerate(df_socios.nome.values):
        aux += capitalize_name(n)
        if i < tam:
            aux += "\n"

    nome = [
        [sg.T("Nome")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_socios.cpf.values):
        aux += n
        if i < tam:
            aux += "\n"

    cpf = [
        [sg.T("CPF")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_socios.plano_assinado.values):
        aux += n.capitalize()
        if i < tam:
            aux += "\n"

    plano_assinado = [
        [sg.T("Plano Assinado")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_socios.email.values):
        aux += n
        if i < tam:
            aux += "\n"

    email = [
        [sg.T("Email")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_socios.telefone.values):
        aux += n
        if i < tam:
            aux += "\n"

    telefone = [
        [sg.T("Telefone")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_socios.endereco.values):
        aux += n
        if i < tam:
            aux += "\n"

    endereco = [
        [sg.T("Endereco")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_socios.data_associacao.values):
        aux += str(n)[:10]
        if i < tam:
            aux += "\n"

    data_associacao = [
        [sg.T("Data Associacao")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_socios.data_desativacao.values):
        if not pd.isnull(n):
            aux += str(n)[:10]
        else:
            aux += "N/A"
        if i < tam:
            aux += "\n"

    data_desativacao = [
        [sg.T("Data Desativacao")],
        [sg.T(aux)]
    ]

    cols = [
        [
            sg.Col(nome, p=(0, 0)),
            sg.Col(cpf, p=(0, 0)),
            sg.Col(plano_assinado, p=(0, 0)),
            sg.Col(email, p=(0, 0)),
            sg.Col(telefone, p=(0, 0)),
            sg.Col(endereco, p=(0, 0)),
            sg.Col(data_associacao, p=(0, 0)),
            sg.Col(data_desativacao, p=(0, 0))
        ]
    ]

    layout = [
        [sg.Column(cols, scrollable=True, vertical_scroll_only=True, p=(0, 0), size_subsample_height=1.5)],
        [sg.B("    OK    ")]
    ]

    window = sg.Window("Socios", layout, element_justification="center")

    window.read(close=True)

def relatorio_planos():
    df_planos = relatorios.get_relatorio_planos()
    tam = len(df_planos.nome.values)-1

    aux = ""
    for i, n in enumerate(df_planos.nome.values):
        aux += n.capitalize()
        if i < tam:
            aux += "\n"

    nome = [
        [sg.T("Nome")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_planos.valor.values):
        aux += str(n)
        if i < tam:
            aux += "\n"

    valor = [
        [sg.T("Valor")],
        [sg.T(aux)]
    ]
    cols = [
        [
            sg.Col(nome, p=(0, 0)),
            sg.Col(valor, p=(0, 0))
        ]
    ]

    layout = [
        [sg.Column(cols)],
        [sg.B("    OK    ")]
    ]

    window = sg.Window("Planos", layout, element_justification="center")

    window.read(close=True)

def relatorio_socios_por_plano():
    df_socios_por_plano = relatorios.get_relatorio_socios_por_plano()
    tam = len(df_socios_por_plano.nome_plano.values)-1

    aux = ""
    for i, n in enumerate(df_socios_por_plano.nome_plano.values):
        aux += n.capitalize()
        if i < tam:
            aux += "\n"

    nome_plano = [
        [sg.T("Nome Plano")],
        [sg.T(aux)]
    ]

    aux = ""
    for i, n in enumerate(df_socios_por_plano.qtd_socios.values):
        aux += str(n)
        if i < tam:
            aux += "\n"

    qtd_socios = [
        [sg.T("Qtd Socios")],
        [sg.T(aux)]
    ]
    cols = [
        [
            sg.Col(nome_plano, p=(0, 0)),
            sg.Col(qtd_socios, p=(0, 0))
        ]
    ]

    layout = [
        [sg.Column(cols)],
        [sg.B("    OK    ")]
    ]

    window = sg.Window("Socios Por Plano", layout, element_justification="center")

    window.read(close=True)

def run():
    tela_inicial.get_updated_screen()

    layout_relatorios = [
        [sg.B("Socios", k='-R_S-', expand_x=True)],
        [sg.B("Planos", k='-R_P-', expand_x=True)],
        [sg.B("Socios por Plano", k='-R_S/P-', expand_x=True)]
    ]
    layout_inserir = [
        [sg.B("Socios", k='-I_S-', expand_x=True)],
        [sg.B("Planos", k='-I_P-', expand_x=True)]
    ]
    layout_atualizar = [
        [sg.B("Socios", k='-A_S-', expand_x=True)],
        [sg.B("Planos", k='-A_P-', expand_x=True)]
    ]
    layout_excluir = [
        [sg.B("Socios", k='-E_S-', expand_x=True)],
        [sg.B("Planos", k='-E_P-', expand_x=True)]
    ]
    tab_group = [
        [sg.Tab("Relatorios", layout_relatorios)],
        [sg.Tab("Inserir", layout_inserir)],
        [sg.Tab("Atualizar", layout_atualizar)],
        [sg.Tab("Excluir", layout_excluir)]
    ]
    layout = [
        [sg.TabGroup(tab_group, tab_background_color="#64778d", expand_y=True)],
        [sg.Col([[sg.B("    Sair    ", k='-SAIR-')]], element_justification="right", expand_x=True, pad=(0,0))]
    ]
    window = sg.Window("Sócios Torcedores - SC/BR, layout)

    while True:
        event, values = window.read()
        if event in ("-SAIR-", sg.WINDOW_CLOSED):
            break
        elif event == '-R_S-':
            relatorio_socios()
        elif event == '-R_P-':
            relatorio_planos()
        elif event == '-R_S/P-':
            relatorio_socios_por_plano()
        elif event == '-I_S-':
            ctrl_socios.inserir_socio()
        elif event == '-I_P-':
            ctrl_planos.inserir_plano()
        elif event == '-A_S-':
            ctrl_socios.atualizar_socio()
        elif event == '-A_P-':
            ctrl_planos.atualizar_plano()
        elif event == '-E_S-':
            ctrl_socios.excluir_socio()
        elif event == '-E_P-':
            ctrl_planos.excluir_plano()
    window.close()

if __name__ == "__main__":
    run()