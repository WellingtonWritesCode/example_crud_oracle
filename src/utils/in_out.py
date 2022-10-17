import PySimpleGUI as sg
import re

def le_int(texto:str="Insira um numero:") -> int:

    window = sg.Window("Entrada", [[sg.T(texto)],
                                   [sg.Input(s=(20, 1), key='-IN-'), sg.B('OK', key='-OK-')]])

    while True:

        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            return 0
        elif event == '-OK-':
            try:
                out = int(values['-IN-'])
                window.close()
                return out
            except ValueError:
                sg.PopupOK("Numero invalido!")

def le_cpf(texto: str = ""):

    window = sg.Window("Entrada", [[sg.T(texto)],
                                   [sg.Input(s=(20, 1), key='-IN-'), sg.B('Cancelar', key='-CANCEL-'), sg.B('OK', key='-OK-')]])

    while True:

        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, '-CANCEL-'):
            return None
        elif event == '-OK-':
            cpf = values['-IN-']
            if re.match("[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}", cpf):
                window.close()
                return cpf
            elif re.match("[0-9]{11}", cpf):
                window.close()
                return f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
            else:
                sg.PopupOK("CPF invalido!")

if __name__ == "__main__":
    print(le_cpf())
