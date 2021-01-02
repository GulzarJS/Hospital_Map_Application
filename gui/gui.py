# hello_world.py
import pandas as pd
import PySimpleGUI as sg
from source import networks

data = networks.getData("../data_parser/data/datas.csv")
dataHospitals = networks.getData("../data_parser/data/datasHospitals.csv")
allSource = networks.getSource()
hospitals = networks.getHospitals()

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
    [sg.Text('Enter Source '), sg.InputCombo(tuple(hospitals.keys()), size=(40, 1), key='source')],
    [sg.Text('Enter Target '), sg.InputCombo(tuple(hospitals.keys()), size=(40, 1), key='dest')],
    [sg.Button('Go'), sg.Button('Exit')]
]

path_layout = [
    # [sg.Text('Network Algorithms Final Project', size=(25, 1), justification='center', font=("Helvetica", 16),
    #          relief=sg.RELIEF_RIDGE)],
    [sg.Frame('Path', [[
        sg.Text('path', size=(35, 3), justification='left', font=("Helvetica", 10), key='-PATH-')]])],
    [sg.Frame('Distance', [[
        sg.Text('distance', size=(25, 1), justification='left', font=("Helvetica", 10), key='-DISTANCE-')]])],
    [sg.Frame('Car', [[
        sg.Text('time', size=(25, 1), justification='left', font=("Helvetica", 10), key='-CAR-')]])],
    [sg.Frame('Bicycle', [[
        sg.Text('distance', size=(25, 1), justification='left', font=("Helvetica", 10), key='-BICYCLE-')]])],
    [sg.Frame('Pedestrian', [[
        sg.Text('distance', size=(25, 1), justification='left', font=("Helvetica", 10), key='-PEDESTRIAN-')]])],
    [sg.Button('Go To Map')]
]


layout = [[sg.TabGroup([[sg.Tab('Map', map_layout), sg.Tab('Path', path_layout)]], key='Tabs')]]

window = sg.Window("Hospital Map Application", layout, default_element_size=(40, 1), grab_anywhere=False, size=(800, 600))

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
    if event == 'Go To Map':
        window['Map'].select()

    if event == 'Go':
        path = networks.shortestPath(hospitals.get(values['source']), hospitals.get(values['dest']))
        distance = networks.findDistance(hospitals.get(values['source']),hospitals.get(values['dest']))

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

        # window.bind(str(path),, 'Path')
        print(path)
        window['-PATH-'].update(str(path))
        window['-DISTANCE-'].update(str((distance * 1000).__round__(2)))
        window['-CAR-'].update(networks.getCarTime(distance * 1000).__round__(2))
        window['-BICYCLE-'].update(networks.getBicycleTime(distance * 1000).__round__(2))
        window['-PEDESTRIAN-'].update(networks.getPedestrianTime(distance * 1000).__round__(2))
        window.refresh()
        window['Path'].select()
        continue
