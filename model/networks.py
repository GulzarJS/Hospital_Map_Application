import networkx as nx
import pandas as pd


# Function to get DataFrame from file
def getData(filename):
    # reading data from file
    data = pd.read_csv(filename)
    return data


# Function to get nodes of hospitals
def getHospitals():
    # getting DataFrame from file
    data = getData("../data_parser/data/datasHospitals.csv")
    # declaring dictionary for holding name of hospitals and node_id of their nearestWayNode
    hospitals = dict()
    # initialising hospital dictionary
    for i in range(0, len(data)):
        hospitals[data.at[i, 'name']] = data.at[i, 'nearestWayNode']
    return hospitals


# Function to get shortest path between given nodes
def shortestPath(source, destination):
    # getting DataFrame from file
    data = getData("../data_parser/data/datas.csv")
    # creating graph of nodes
    G = nx.from_pandas_edgelist(data, source='a_node_id', target='b_node_id', edge_attr=True, create_using=nx.DiGraph)
    # finding shortest path by using function of networkx library
    path = nx.shortest_path(G, source, destination, weight="distance")
    return path


# Function to get distance of shortest path between given nodes
def findDistance(source, destination):
    # getting DataFrame from file
    data = getData("../data_parser/data/datas.csv")
    # creating graph of nodes
    G = nx.from_pandas_edgelist(data, source='a_node_id', target='b_node_id', edge_attr=True, create_using=nx.DiGraph)
    # finding lenght of shortest path by using function of networkx library
    distance = nx.dijkstra_path_length(G, source, destination, weight="distance")
    return distance


# Function to get duration of trip by car
def getCarTime(distance):
    # m per second
    speed = 16.7
    time = distance / speed
    # convert seconds to minutes
    time = time / 60
    return time


# Function to get duration of trip by bicycle
def getBicycleTime(distance):
    # m per second
    speed = 6.95
    time = distance / speed
    # convert seconds to minutes
    time = time / 60
    return time


# Function to get duration of trip on foot
def getPedestrianTime(distance):
    # m per second
    speed = 1.39
    time = distance / speed
    # convert seconds to minutes
    time = time / 60
    return time


# Function to draw map in gui
def drawLine(graph):
    # declaring dictionaries for holding points and lines of map graph
    waysLinesBlack = {}
    waysLinesRed = {}
    hospitalsPoints = {}
    # getting DataFrames from files
    data = getData("../data_parser/data/datas.csv")
    dataHospitals = getData("../data_parser/data/datasHospitals.csv")

    # drawing red line for shortest path
    for i in range(len(data)):
        waysLinesRed[str(data.at[i, 'a_node_id']) + "," + str(data.at[i, 'b_node_id'])] = graph.DrawLine(
            ((data.at[i, 'a_node_lon'] - 49.8291) * 10000, (data.at[i, 'a_node_lat'] - 40.3691) * 14000),
            ((data.at[i, 'b_node_lon'] - 49.8291) * 10000, (data.at[i, 'b_node_lat'] - 40.3691) * 14000), color='red')

    # drawing black lines for all paths
    for i in range(len(data)):
        waysLinesBlack[str(data.at[i, 'a_node_id']) + "," + str(data.at[i, 'b_node_id'])] = graph.DrawLine(
            ((data.at[i, 'a_node_lon'] - 49.8291) * 10000, (data.at[i, 'a_node_lat'] - 40.3691) * 14000),
            ((data.at[i, 'b_node_lon'] - 49.8291) * 10000, (data.at[i, 'b_node_lat'] - 40.3691) * 14000))

    # drawing red circles for hospital nodes
    for i in range(len(dataHospitals)):
        hospitalsPoints[str(dataHospitals.at[i, 'node_id'])] = graph.DrawCircle(
            ((dataHospitals.at[i, 'lon'] - 49.8291) * 10000, (dataHospitals.at[i, 'lat'] - 40.3691) * 14000), 3,
            fill_color='red')
    # return only red line
    return waysLinesRed
