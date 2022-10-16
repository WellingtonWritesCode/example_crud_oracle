import PySimpleGUI as sg


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

if __name__ == "__main__":
    sg.PopupOK("Test", 1)