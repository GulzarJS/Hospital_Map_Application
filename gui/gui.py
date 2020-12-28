# hello_world.py

import PySimpleGUI as sg

menu_def = [['&Map'],
            ['&Path']]


# ------ Column Definition ------ #
column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [sg.Text('Network Algorithms Final Project', size=(25, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
    [sg.Frame(layout=[[sg.Image(r'map.png')]], title='Map', title_color='magenta', relief=sg.RELIEF_SUNKEN,
        tooltip='Use these to set flags')],
    [sg.Text('Enter Source '), sg.InputCombo(('Baku', 'Shamakhi', 'Kurdemir', 'Goychay'), size=(20, 1))],
    [sg.Text('Enter Source '),sg.InputCombo( ('Baku', 'Shamakhi', 'Kurdemir', 'Goychay'), size=(20, 1))],
    [sg.Button('Go'), sg.Button('Exit')]]


window = sg.Window("Shortest Path Application",  layout, default_element_size=(40, 1), grab_anywhere=False)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

event, values = window.read()
window.close()