import PySimpleGUI as sg

tab1=sg.Tab('Tab 1', [[sg.Text("Tab1")],])
tab2=sg.Tab('Tab 2', [[sg.Text("Tab2")],])

layout = [  [sg.Text("title    "),sg.Text("index")],
            [sg.Input(key="_text_",size=(5,1)), sg.Input(key="_index_",size=(5,1))],
            [sg.TabGroup([[tab1,tab2]], key='_TAB_GROUP_')],
            [sg.Button("change title")],[sg.Button("Exit")]]

window = sg.Window("Tabs", layout)

while True:
    event, values = window.Read()
    if event in  (None, "Exit"):
        break
    elif event == "change title":
        window.Element('_TAB_GROUP_').Widget.tab(int(values["_index_"]),text=values["_text_"])

window.Close()