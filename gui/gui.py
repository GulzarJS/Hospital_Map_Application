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
    [sg.Text('Enter Source ',  size = (10, 1), font=("Helvetica", 12)), sg.InputCombo(tuple(hospitals.keys()), size=(38, 1), key='source'),
     sg.Text('Enter Target ',  size = (10, 1), font=("Helvetica", 12)), sg.InputCombo(tuple(hospitals.keys()), size=(38, 1), key='dest')],
    [sg.Button('Go', size = (10, 1), font=("Helvetica", 12)), sg.Button('Exit',  size = (10, 1), font=("Helvetica", 12))]
]

path_layout = [
    # [sg.Text('Network Algorithms Final Project', size=(25, 1), justification='center', font=("Helvetica", 16),
    #          relief=sg.RELIEF_RIDGE)],
    [sg.Frame('Distance',  [[
        sg.Text('distance', size=(100, 2), justification='left', font=("Helvetica", 13), key='-DISTANCE-')]] , size = (13, 2), font=("Helvetica", 15))],
    [sg.Frame('Car', [[
        sg.Text('time', size=(100, 2), justification='left', font=("Helvetica", 13), key='-CAR-')]], size = (13, 2), font=("Helvetica", 15))],
    [sg.Frame('Bicycle', [[
        sg.Text('time', size=(100, 2), justification='left', font=("Helvetica", 13), key='-BICYCLE-')]], size = (13, 2), font=("Helvetica", 15))],
    [sg.Frame('Pedestrian', [[
        sg.Text('time', size=(100, 2), justification='left', font=("Helvetica", 13), key='-PEDESTRIAN-')]], size = (13, 2), font=("Helvetica", 15))],
    [sg.Button('Go To Map', size = (10, 1), font=("Helvetica", 12))]
]


layout = [[sg.TabGroup([[sg.Tab('Map', map_layout), sg.Tab('Path', path_layout)]], key='Tabs')]]

window = sg.Window("Hospital Map Application", layout, default_element_size=(40, 1), grab_anywhere=False, size=(800, 550))

window.Finalize()

graph = window['graph']
waysLinesBlack = {}
waysLinesRed = {}
hospitalsPoints = {}


for i in range(len(data)):
    waysLinesRed[str(data.at[i, 'a_node_id']) + "," + str(data.at[i, 'b_node_id'])] = graph.DrawLine(((data.at[i, 'a_node_lon'] - 49.8291) * 10000, (data.at[i, 'a_node_lat']-40.3691)*14000), ((data.at[i, 'b_node_lon'] - 49.8291) * 10000, (data.at[i, 'b_node_lat']-40.3691)*14000), color='red')


for i in range(len(data)):
    waysLinesBlack[str(data.at[i, 'a_node_id']) + "," + str(data.at[i, 'b_node_id'])] = graph.DrawLine(((data.at[i, 'a_node_lon'] - 49.8291) * 10000, (data.at[i, 'a_node_lat']-40.3691)*14000), ((data.at[i, 'b_node_lon'] - 49.8291) * 10000, (data.at[i, 'b_node_lat']-40.3691)*14000))

for i in range(len(dataHospitals)):
    hospitalsPoints[str(dataHospitals.at[i, 'node_id'])] = graph.DrawCircle(((dataHospitals.at[i, 'lon'] - 49.8291) * 10000, (dataHospitals.at[i, 'lat'] - 40.3691) * 14000), 3, fill_color='red')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Go To Map':
        window['Map'].select()

    if event == 'Go':

        try:
            path = networks.shortestPath(hospitals.get(values['source']), hospitals.get(values['dest']))
            distance = networks.findDistance(hospitals.get(values['source']), hospitals.get(values['dest']))

            for el in waysLinesRed:
                graph.SendFigureToBack(waysLinesRed[el])

            firstNodeFlag = True
            firstNode = ""
            for i in range(len(path)):
                if firstNodeFlag:
                    firstNode = path[i]
                    firstNodeFlag = False
                    continue

                graph.BringFigureToFront(waysLinesRed[str(firstNode) + "," + str(path[i])])

                firstNode = path[i]
                window.refresh()


            print("Distance between ", values['source'], " and ", values['dest'])
            print(path)
            window['-DISTANCE-'].update(str((distance).__round__(2)) + " meters")
            window['-CAR-'].update(str(networks.getCarTime(distance).__round__(2)) + " minutes")
            window['-BICYCLE-'].update(str(networks.getBicycleTime(distance).__round__(2)) + " minutes")
            window['-PEDESTRIAN-'].update(str(networks.getPedestrianTime(distance).__round__(2)) + " minutes")
            window.refresh()
            continue
        except Exception as e:
            sg.Popup('No path found', 'Due to lack of the necessary nodes in datasets we could not find a path between \" ' + values['source'] + ' \" and \" ' + values['dest'] + ' \"')
            continue

