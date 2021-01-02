# hello_world.py
import pandas as pd
import PySimpleGUI as sg
from source import networks

data = pd.read_csv('../data_parser/data/datas.csv')
dataHospitals = pd.read_csv("../data_parser/data/datasHospitals.csv")

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
    # [sg.Frame(layout=[[sg.Image(r'map.png')]], title='Map', title_color='magenta', relief=sg.RELIEF_SUNKEN,
    #           tooltip='Use these to set flags')],
    [sg.Graph(canvas_size=(800, 400), graph_bottom_left=(0,0), graph_top_right=(400, 200), background_color='lightgray', key='graph')],
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

window = sg.Window("Hospital Map Application", layout, default_element_size=(40, 1), grab_anywhere=False, size=(1000, 800))

window.Finalize()

graph = window['graph']
waysLinesBlack = {}
waysLinesGreen = {}
hospitalsPoints = {}


for i in range(len(data)):
    waysLinesGreen[str(data.at[i, 'a_node_id']) + ","+ str(data.at[i, 'b_node_id'])] = graph.DrawLine(((data.at[i, 'a_node_lon'] - 49.8291) * 10000, (data.at[i, 'a_node_lat']-40.3691)*14000), ((data.at[i, 'b_node_lon'] - 49.8291) * 10000, (data.at[i, 'b_node_lat']-40.3691)*14000), color='green')


for i in range(len(data)):
    waysLinesBlack[str(data.at[i, 'a_node_id']) + ","+ str(data.at[i, 'b_node_id'])] = graph.DrawLine(((data.at[i, 'a_node_lon'] - 49.8291) * 10000, (data.at[i, 'a_node_lat']-40.3691)*14000), ((data.at[i, 'b_node_lon'] - 49.8291) * 10000, (data.at[i, 'b_node_lat']-40.3691)*14000))

for i in range(len(dataHospitals)):
    hospitalsPoints[str(dataHospitals.at[i, 'node_id'])] = graph.DrawCircle(((dataHospitals.at[i, 'lon'] - 49.8291) * 10000, (dataHospitals.at[i, 'lat'] - 40.3691) * 14000), 3, fill_color='red')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Go':
        path = networks.shortestPath(data, values['source'], values['dest'])

        for el in waysLinesGreen:
            graph.SendFigureToBack(waysLinesGreen[el])

        firstNodeFlag = True
        firstNode = ""
        for i in range(len(path)):
            if firstNodeFlag:
                firstNode = path[i]
                firstNodeFlag = False
                continue
            
            graph.BringFigureToFront(waysLinesGreen[str(firstNode)+","+str(path[i])])

            firstNode = path[i]

        distance = networks.findDistance(data, values['source'], values['dest'])
        # window.bind(str(path),, 'Path')
        print(path)
        window['-PATH-'].update(str(path))
        window['-DISTANCE-'].update(str(distance))
        window.refresh()
        window['Path'].select()
        continue
