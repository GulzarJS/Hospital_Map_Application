# hello_world.py
import PySimpleGUI as sg
import networks

# hospital nodes
hospitals = networks.getHospitals()

# shortest path
path = tuple()


# ------ Column Definition ------ #
column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]


# 'Map' tab of window for taking source and target nodes and showing path of map in red color
map_layout = [
    # map
    [sg.Graph(canvas_size=(800, 400), graph_bottom_left=(0, 0), graph_top_right=(400, 200),
              background_color='lightgray', key='graph')],

    # getting name of source and target node
    [sg.Text('Enter Source ', size=(10, 1), font=("Helvetica", 12)),
     sg.InputCombo(tuple(hospitals.keys()), size=(38, 1), key='source'),
     sg.Text('Enter Target ', size=(10, 1), font=("Helvetica", 12)),
     sg.InputCombo(tuple(hospitals.keys()), size=(38, 1), key='dest')],

    # Go and Exit button
    [sg.Button('Go', size=(10, 1), font=("Helvetica", 12)), sg.Button('Exit', size=(10, 1), font=("Helvetica", 12))]
]


# 'Path' tab of window for showing distance between 2 nodes and duration of the trip,
# taking into account speed of person (car, bicycle, pedestrian)
path_layout = [
    # Calculations for shortest path
    [sg.Frame('Distance', [[
        sg.Text('distance', size=(100, 2), justification='left', font=("Helvetica", 13), key='-DISTANCE-')]],
              size=(13, 2), font=("Helvetica", 15))],
    [sg.Frame('Car', [[
        sg.Text('time', size=(100, 2), justification='left', font=("Helvetica", 13), key='-CAR-')]], size=(13, 2),
              font=("Helvetica", 15))],
    [sg.Frame('Bicycle', [[
        sg.Text('time', size=(100, 2), justification='left', font=("Helvetica", 13), key='-BICYCLE-')]], size=(13, 2),
              font=("Helvetica", 15))],
    [sg.Frame('Pedestrian', [[
        sg.Text('time', size=(100, 2), justification='left', font=("Helvetica", 13), key='-PEDESTRIAN-')]],
              size=(13, 2), font=("Helvetica", 15))],

    # 'Go To Map' button for directly showing map of city and shortest path
    [sg.Button('Go To Map', size=(10, 1), font=("Helvetica", 12))]
]

# layout for creating window of application. TabGroup holds 'Map' and 'Path' tabs
layout = [[sg.TabGroup([[sg.Tab('Map', map_layout), sg.Tab('Path', path_layout)]], key='Tabs')]]

# creating application window
window = sg.Window("Hospital Map Application", layout, default_element_size=(40, 1), grab_anywhere=False,
                   size=(800, 550))

# image appears only when updating the Image element after the window has been read
window.Finalize()

# map graph to show shortest map on city map
graph = window['graph']

# drawing city map and returning red line
waysLinesRed = networks.drawLine(graph)


# while window is open
while True:

    # reading window
    event, values = window.read()

    # closing window
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        break

    # directly opening map with 1 button
    if event == 'Go To Map':
        window['Map'].select()

    # finding shortest path and doing calculation of it
    if event == 'Go':

        # if there is shortest path
        try:
            # find path and length of it
            path = networks.shortestPath(hospitals.get(values['source']), hospitals.get(values['dest']))
            distance = networks.findDistance(hospitals.get(values['source']), hospitals.get(values['dest']))

            # drawing red line on city map
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

                # refresh window after drawing
                window.refresh()

            # print path between 2 nodes in terminal
            print("Distance between ", values['source'], " and ", values['dest'])
            print(path)

            # update 'Path' tab with length of shortest path and duration calculations
            window['-DISTANCE-'].update(str((distance).__round__(2)) + " meters")
            window['-CAR-'].update(str(networks.getCarTime(distance).__round__(2)) + " minutes")
            window['-BICYCLE-'].update(str(networks.getBicycleTime(distance).__round__(2)) + " minutes")
            window['-PEDESTRIAN-'].update(str(networks.getPedestrianTime(distance).__round__(2)) + " minutes")

            # refresh window after updating 'Path' tab
            window.refresh()
            continue

        # if there is no path, open pop up information window
        except Exception as e:
            sg.Popup('No path found!', 'Due to lack of the necessary nodes in datasets we could not find a path '
                                      'between \" ' + values['source'] + ' \" and \" ' + values['dest'] + ' \"')
            continue
