import googlemaps as gm
from datetime import datetime

import itertools
import networkx as nx

from flask import Flask, url_for
from flask import request as fr

import os


api_key = os.getenv('GMAPS_API_KEY')
client = gm.Client(key=api_key)

graph = nx.Graph()


def get_distance(loc1, loc2):
    return client.directions(loc1, loc2, mode='driving')\
        [0]['legs'][0]['duration']['value']

def get_coords(address):
    return tuple(client.geocode(address)\
        [0]['geometry']['location'].values())

def add_node(g, addr, b, e, pay):
    g.add_node(addr, coords=get_coords(addr), payment=0, begin=b, end=e)
    for v in g.nodes(data=True):
        if (v[0] != addr):
            g.add_edge(addr, v[0], weight=get_distance(
                g.nodes()[addr]['coords'], v[1]['coords']))

def find_path(spos, stime, dur, work_time, price_of_minute=7, portion_of_payment=0.1):
    etime = stime + dur
    g = graph.copy()
    add_node(g, spos, 0, stime, 0)
    path = []
    curr = spos
    neighbors = set(n for n in nx.neighbors(g, curr) if g.get_edge_data(curr, n)['weight'] + work_time < dur)
    def should_go(u, v):
        if v in path:
            return False
        arrival_time = stime + g.get_edge_data(u, v)['weight']
        finish_time = arrival_time + work_time
        if (arrival_time < g.nodes(data=True)[v]['begin'] or finish_time > g.nodes(data=True)[v]['end']):
            return False
        if finish_time > etime:
            return False
        return True
    while True:
        path.append(curr)
        if not neighbors:
            return [g.nodes(data=True)[n]['coords'] for n in path]
        curr = min(neighbors,
                   key=lambda x: g.get_edge_data(curr, x)['weight'] 
                                 - portion_of_payment
                                 * g.nodes(data=True)[curr]['payment'])
        neighbors = set(n for n in nx.neighbors(g, curr) if should_go(curr, n))


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/place_addresses', methods=['POST'])
def place_addresses():
    addr = fr.get_json()['addr']
    print(addr)
    for a, b, e, p in addr:
        add_node(graph, a, b, e, p)
    from pprint import pprint
    pprint(graph.nodes(data=True))
    return 'OK'

@app.route('/remove', methods=['POST'])
def remove():
    addr = fr.json['addr']
    if type(addr) is str:
        graph.remove_node(addr)
    elif type(addr) is list:
        graph.remove_nodes_from(addr)
    return 'OK'

@app.route('/get_path', methods=['GET'])
def get_path():
    spos = fr.json['spos']
    stime = fr.json['stime']
    dur = fr.json['dur']
    wt = fr.json['wt']
    return str(find_path(spos, stime, dur, wt))


app.run(host="0.0.0.0", port=8080)
