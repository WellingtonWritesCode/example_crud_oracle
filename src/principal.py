import PySimpleGUI as sg
from utils.splash_screen import SplashScreen
from controller.controller_planos import Controller_Planos

tela_inicial = SplashScreen()
ctrl_planos = Controller_Planos()

def run():
    tela_inicial.get_updated_screen()

    layout_relatorios = [
        []
    ]
    layout_inserir = [
        [sg.B("Socios", k='-I_S-', enable_events=True)],
        [sg.B("Planos", k='-I_P-', enable_events=True)],
        [sg.B("Mensalidades", k='-I_M-', enable_events=True)]
    ]
    layout_atualizar = [
        [sg.B("Socios", k='-A_S-', enable_events=True)],
        [sg.B("Planos", k='-A_P-', enable_events=True)],
        [sg.B("Mensalidades", k='-A_M-', enable_events=True)]
    ]
    layout_excluir = [
        [sg.B("Socios", k='-E_S-', enable_events=True)],
        [sg.B("Planos", k='-E_P-', enable_events=True)],
        [sg.B("Mensalidades", k='-E_M-', enable_events=True)]
    ]
    tab_group = [
        [sg.Tab("Relatorios", layout_relatorios)],
        [sg.Tab("Inserir Novos Registros", layout_inserir)],
        [sg.Tab("Atualizar Registros", layout_atualizar)],
        [sg.Tab("Excluir Registros", layout_excluir)]
    ]
    layout = [
        [sg.TabGroup(tab_group, tab_background_color="#64778d", expand_y=True)],
        [sg.Col([[sg.B("    Sair    ", k='-SAIR-')]], element_justification="right", expand_x=True, pad=(0,0))]
    ]
    window = sg.Window("SCSTSCB", layout)

    while True:
        event, values = window.read()
        if event in ("-SAIR-", sg.WINDOW_CLOSED):
            break
        elif event == '-I_S-':
            pass
        elif event == '-I_P-':
            ctrl_planos.inserir_plano
        elif event == '-I_M-':
            pass
        elif event == '-A_S-':
            pass
        elif event == '-A_P-':
            ctrl_planos.atualizar_plano
        elif event == '-A_M-':
            pass
        elif event == '-E_S-':
            pass
        elif event == '-E_P-':
            ctrl_planos.excluir_plano
        elif event == '-E_M-':
            pass
    window.close()

if __name__ == "__main__":
    run()