import networkx as nx
import pandas as pd


# Function to get DataFrame from file
def getData(filename):
    data = pd.read_csv(filename)
    return data


# Function to get source nodes from file
def getSource():
    data = getData("../data_parser/data/datas.csv")
    sourcesList = list()
    for i in range(0, len(data)):
        sourcesList.append(data.at[i, 'a_node_id'])
    source = tuple(sourcesList)
    return source


# Function to get nodes of hospitals
def getHospitals():
    data = getData("../data_parser/data/datasHospitals.csv")
    hospitals = dict()
    for i in range(0, len(data)):
        hospitals[data.at[i, 'name']] = data.at[i, 'nearestWayNode']

    return hospitals


# Function to get shortest path between given nodes
def shortestPath(source, destination):
    data = getData("../data_parser/data/datas.csv")
    G = nx.from_pandas_edgelist(data, source='a_node_id', target='b_node_id', edge_attr=True, create_using=nx.DiGraph)
    path = nx.shortest_path(G, source, destination, weight="distance")

    return path


# Function to get distance of shortest path between given nodes
def findDistance(source, destination):
    data = getData("../data_parser/data/datas.csv")
    G = nx.from_pandas_edgelist(data, source='a_node_id', target='b_node_id', edge_attr=True, create_using=nx.DiGraph)
    distance = nx.dijkstra_path_length(G, source, destination, weight="distance")
    return distance


# Function to get time of travel by car
def getCarTime(distance):
    speed = 50  # km per hour
    time = distance / speed
    return time


# Function to get time of travel by bicycle
def getBicycleTime(distance):
    speed = 25  # km per hour
    time = distance / speed
    return time


# Function to get time of travel on foot
def getPedestrianTime(distance):
    speed = 5  # km per hour
    time = distance / speed
    return time
