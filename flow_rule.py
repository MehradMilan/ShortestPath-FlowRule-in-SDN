import requests
import random
import json
import networkx as nx

FLOODLIGHT_URL = 'http://127.0.0.1:8080'

def get_topology():
    api_call = f'{FLOODLIGHT_URL}/wm/topology/links/json'
    response = requests.get(api_call)
    return response.json()

def assign_weights(topology):
    for link in topology:
        link['weight'] = random.randint(1, 10)
    return topology

def build_graph(topology):
    G = nx.Graph()
    for link in topology:
        src = link['src-switch']
        dst = link['dst-switch']
        G.add_edge(src, dst, weight=link['weight'])
    return G

def find_shortest_path(src, dst, topology):
    G = build_graph(topology)
    path = nx.dijkstra_path(G, src, dst, weight='weight')
    return path

def generate_flow_rules(path):
    rules = []
    for i in range(len(path)-1):
        src = path[i]
        dst = path[i+1]

        rule = {
            "switch": src,
            "name":"flow-mod-1",
            "cookie":"0",
            "priority":"32768",
            "in_port":"ANY",
            "eth_type":"0x800",
            "ipv4_src":path[0],
            "ipv4_dst":path[-1],
            "ip_proto":"0x06",
            "tcp_src":"ANY",
            "tcp_dst":"ANY",
            "active":"true",
            "actions":"output=" + str(dst)
        }
        rules.append(rule)

    return rules


def push_flow_rules(rules):
    api_call = f'{FLOODLIGHT_URL}/wm/staticentrypusher/json'
    for rule in rules:
        response = requests.post(api_call, data=json.dumps(rule))

if __name__ == "__main__":
    topology = get_topology()
    topology = assign_weights(topology)
    src_inp = input('Type the source Host: (Number between 1 to 8)')
    src = '00:00:00:00:00:00:00:0' + str(src_inp)  # replace with actual switch id
    dst_inp = input('Type the Destination Host: (Number between 1 to 8)')
    dst = '00:00:00:00:00:00:00:0' + str(dst_inp)  # replace with actual switch id
    shortest_path = find_shortest_path(src, dst, topology)
    print(shortest_path)
    flow_rules = generate_flow_rules(shortest_path)
    push_flow_rules(flow_rules)
