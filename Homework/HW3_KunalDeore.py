# Assignment 3: 
# Kunal Deore
# 
# -------------------------------------------
#

# Import the libraries
import heapq
import copy

class Node(object):

    def __init__(self, name):
        self.name = name
        self.connected_nodes = {}
        self.distance = float('inf')
        self.visited = False
        self.previous = None

    def add_connection(self, neighbor, weight=0):
        self.connected_nodes[neighbor] = weight

    def get_connections(self):
        return self.connected_nodes.keys()

    def get_name(self):
        return self.name

    def get_weight(self, neighbor):
        return self.connected_nodes[neighbor]

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def set_previous(self, previous):
        self.previous = previous

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return f'{self.name}: {[x.id for x in self.connected_nodes]}'

    def __lt__(self, other):
        return self.distance < other.distance
    
class Network(object):

    def __init__(self):
        self.node_dict = {}
        self.num_nodes = len(self.node_dict)
        self.previous = None

    def __iter__(self):
        return iter(self.node_dict.values())

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_node(self, node):
        self.node_dict[node] = Node(node)
        self.num_nodes = len(self.node_dict)
        return self.node_dict[node]

    def get_node(self, n):
        return self.node_dict[n] if n in self.node_dict else None

    def add_edge(self, frm, to, edge_weight=0.0):
        if frm not in self.node_dict:
            self.add_node(frm)
        if to not in self.node_dict:
            self.add_node(to)

        self.node_dict[frm].add_connection(self.node_dict[to], edge_weight)
        self.node_dict[to].add_connection(self.node_dict[frm], edge_weight)

    def get_nodes(self):
        return list(self.node_dict.keys())

    def set_previous(self, current):
        self.previous = current

    def get_previous(self):
        return self.previous

    def __str__(self):
        text = 'Network\n'
        for node in self:
            for connected_node in node.get_connections():
                node_name = node.get_name()
                connected_node_name = connected_node.get_name()
                text += f'{node_name} -> {connected_node_name} :' \
                        f' {node.get_weight(connected_node)}\n'
        return text
    
class Dijkstra(object):

    @staticmethod
    def compute(network, start):
        start.set_distance(0)

        # create the priority queue with nodes
        unvisited_queue = [(node.get_distance(), node) for node in network] 
        heapq.heapify(unvisited_queue) 

        while len(unvisited_queue):
            # pop a node with the smallest distance
            unvisited_node = heapq.heappop(unvisited_queue)
            current_node = unvisited_node[1]  
            current_node.set_visited()

            for next_node in current_node.connected_nodes:
                if not next_node.visited:
                    new_dist = current_node.get_distance() + current_node.get_weight(next_node)
                    if new_dist < next_node.get_distance():
                        next_node.set_distance(new_dist)
                        next_node.set_previous(current_node)

            # Rebuild heap: Pop every item, Put all nodes not visited into the queue
            while len(unvisited_queue):
                heapq.heappop(unvisited_queue)
            unvisited_queue = [(n.get_distance(), n) for n in network if not n.visited]
            heapq.heapify(unvisited_queue)

    @staticmethod
    def compute_shortest_path(node, path):
        if node.previous:
            path.append(node.previous.get_name())
            Dijkstra.compute_shortest_path(node.previous, path)

def read_network_from_file(file_name, delimeter=','):
    cities = list()
    distances = dict()

    f = open(file_name, 'r')
    lines = f.readlines()
    
    ### Exercise 1 ### 
    #
    # Add more information to the code
    lines.append('New Orleans, Dallas, 505\n')
    lines.append('New Orleans, St. Louis, 677\n')
    lines.append('St. Louis, Chicago, 298\n')
    lines.append('St. Louis, Denver, 298\n')
    
    for line in lines:
        fields = line.rstrip().split(delimeter)
        city_1 = fields[0].strip(' ')
        city_2 = fields[1].strip(' ')
        distance = float(fields[2])

        # build the list of nodes
        if city_1 not in cities:
            cities.append(city_1)
        if city_2 not in cities:
            cities.append(city_2)

        # build the dictionary based on node weights
        if cities.index(city_1) not in distances.keys():
            distances[cities.index(city_1)] = {cities.index(city_2): distance}
        if cities.index(city_2) not in distances[cities.index(city_1)].keys():
            distances[cities.index(city_1)][cities.index(city_2)] = distance

    return cities, distances

def main():
    # application salutation
    #
    application_name = 'Trucking Analysis Network'
    print('-' * len(application_name))
    print(application_name)
    print('-' * len(application_name))

    # read graph from file
    #
    file_name = 'Network.csv'
    cities, distances = read_network_from_file(file_name)

    # build the graph
    #
    network = Network()
    network.add_nodes(cities)
    for connection in distances.items():
        frm = cities[connection[0]]
        for connection_to in connection[1].items():
            network.add_edge(frm, cities[connection_to[0]], connection_to[1])

    # uncomment to print the graph
    # print(network)
    
    # determine the start city
    #
    for (index, city) in enumerate(network.get_nodes()):
        print(f'{index}: {city:s}')
    start_city_index = int(input(
        f'What is the start city by index (0 to {len(network.get_nodes()) - 1})? '))
    start_city = network.get_nodes()[start_city_index]
    
    ### Exercise 2 ###
    #
    hub1_city_index = int(input(
        f'What is the hub1 city by index (0 to {len(network.get_nodes()) - 1})? '))
    hub1_city = network.get_nodes()[hub1_city_index]    
    
    hub2_city_index = int(input(
        f'What is the hub2 city by index (0 to {len(network.get_nodes()) - 1})? '))
    hub2_city = network.get_nodes()[hub2_city_index]

    end_city_index = int(input(
        f'What is the destination city by index (0 to {len(network.get_nodes()) - 1})? '))
    end_city = network.get_nodes()[end_city_index]
    
    # First alternative:
    # using Dijkstra's algorithm, compute least cost (distance)
    
    # from start to hub1 
    network_1 = copy.deepcopy(network)
    Dijkstra.compute(network_1, network_1.get_node(start_city))
    target_city_1 = network_1.get_node(hub1_city)
    path_1 = [target_city_1.get_name()]
    Dijkstra.compute_shortest_path(target_city_1, path_1)
    # print(f'{start_city} -> {hub1_city} = {path_1[::-1]} : {target_city_1.get_distance()}')
    
    # from hub1 to hub2
    network_2 = copy.deepcopy(network)
    Dijkstra.compute(network_2, network_2.get_node(hub1_city))
    target_city_2 = network_2.get_node(hub2_city)
    path_2 = [target_city_2.get_name()]
    Dijkstra.compute_shortest_path(target_city_2, path_2)
    # print(f'{hub1_city} -> {hub2_city} = {path_2[::-1]} : {target_city_2.get_distance()}')
    
    # hub2 to destination
    network_3 = copy.deepcopy(network)
    Dijkstra.compute(network_3, network_3.get_node(hub2_city))
    target_city_3 = network_3.get_node(end_city)
    path_3 = [target_city_3.get_name()]
    Dijkstra.compute_shortest_path(target_city_3, path_3)
    # print(f'{hub2_city} -> {end_city} = {path_3[::-1]} : {target_city_3.get_distance()}')   
    
    # Second alternative:
    # using Dijkstra's algorithm, compute least cost (distance)
    
    # from start to hub2
    network_4 = copy.deepcopy(network)
    Dijkstra.compute(network_4, network_4.get_node(start_city))
    target_city_4 = network_4.get_node(hub2_city)
    path_4 = [target_city_4.get_name()]
    Dijkstra.compute_shortest_path(target_city_4, path_4)
    # print(f'{start_city} -> {hub2_city} = {path_4[::-1]} : {target_city_4.get_distance()}')
    
    # from hub2 to hub1
    network_5 = copy.deepcopy(network)
    Dijkstra.compute(network_5, network_5.get_node(hub2_city))
    target_city_5 = network_5.get_node(hub1_city)
    path_5 = [target_city_5.get_name()]
    Dijkstra.compute_shortest_path(target_city_5, path_5)
    # print(f'{hub2_city} -> {hub1_city} = {path_5[::-1]} : {target_city_5.get_distance()}')
    
    # hub1 to destination
    network_6 = copy.deepcopy(network)
    Dijkstra.compute(network_6, network_6.get_node(hub1_city))
    target_city_6 = network_6.get_node(end_city)
    path_6 = [target_city_6.get_name()]
    Dijkstra.compute_shortest_path(target_city_6, path_6)
    # print(f'{hub1_city} -> {end_city} = {path_6[::-1]} : {target_city_6.get_distance()}')   
    
    # Sum of paths for start_city -> hub1 -> hub2 -> end_city
    sum_1 = target_city_1.get_distance() + target_city_2.get_distance() + target_city_3.get_distance()
    # print(sum_1)
    
    # Sum of paths for start_city -> hub2 -> hub1 -> end_city
    sum_2 = target_city_4.get_distance() + target_city_5.get_distance() + target_city_6.get_distance()
    # print(sum_2)
    
    # Path from start_city -> hub1 -> hub2 -> end_city
    ultimate_path_1 = list(dict.fromkeys(path_1[::-1] + path_2[::-1] + path_3[::-1]))
    # print(ultimate_path_1)
    
    # Path from start_city -> hub2 -> hub1 -> end_city
    ultimate_path_2 = list(dict.fromkeys(path_4[::-1] + path_5[::-1] + path_6[::-1]))
    # print(ultimate_path_2)
    
    # Simple if statement to get print the shortest path and lowest value 
    if sum_1 > sum_2:
        print(f'{start_city} -> {end_city} = {ultimate_path_2} : {sum_2}')
    else: 
        print(f'{start_city} -> {end_city} = {ultimate_path_1} : {sum_1}')
        
if __name__ == '__main__':
    main()