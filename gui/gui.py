# hello_world.py
import pandas as pd
import PySimpleGUI as sg
from source import networks

data = pd.read_csv('../data_parser/data/datas.csv')
source = networks.getSource(data)
destination = networks.getDestination(data)
path = tuple()

# ------ Column Definition ------ #
column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

map_layout = [
    # [sg.Text('Network Algorithms Final Project', size=(25, 1), justification='center', font=("Helvetica", 16),
    #          relief=sg.RELIEF_RIDGE)],
    [sg.Frame(layout=[[sg.Image(r'map.png')]], title='Map', title_color='magenta', relief=sg.RELIEF_SUNKEN,
              tooltip='Use these to set flags')],
    [sg.Text('Enter Source '), sg.InputCombo(source, size=(20, 1), key='source')],
    [sg.Text('Enter Target '), sg.InputCombo(destination, size=(20, 1), key='dest')],
    [sg.Button('Go'), sg.Button('Exit')]
]

path_layout = [
    # [sg.Text('Network Algorithms Final Project', size=(25, 1), justification='center', font=("Helvetica", 16),
    #          relief=sg.RELIEF_RIDGE)],
    [sg.Text('Path:\n', size=(25, 1), justification='left', font=("Helvetica", 10))],
    [sg.Text('path', size=(35, 3), justification='left', font=("Helvetica", 10), key = '-PATH-')],
    [sg.Text('Distance:\n', size=(25, 1), justification='left', font=("Helvetica", 10))],
    [sg.Text('distance', size=(25, 1), justification='left', font=("Helvetica", 10), key = '-DISTANCE-')],
    # [sg.Text('m', size=(25, 1), justification='left', font=("Helvetica", 10), key = '-OUTPUT-')],
    # [sg.Text('m', size=(25, 1), justification='left', font=("Helvetica", 10), key = '-OUTPUT-')],
]

layout = [[sg.TabGroup([[sg.Tab('Map', map_layout), sg.Tab('Path', path_layout)]],key='Tabs')]]

window = sg.Window("Hospital Map Application", layout, default_element_size=(40, 1), grab_anywhere=False)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Go':
        path = networks.shortestPath(data, values['source'], values['dest'])
        distance = networks.findDistance(data, values['source'], values['dest'])
        # window.bind(str(path),, 'Path')
        print(path)
        window['-PATH-'].update(str(path))
        window['-DISTANCE-'].update(str(distance))
        window.refresh()
        window['Path'].select()
        continue
