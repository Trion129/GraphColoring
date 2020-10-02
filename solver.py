#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE
from collections import namedtuple, defaultdict
import multiprocessing
from joblib import Parallel, delayed
import random

def solve_greedy(adjacency_list):
    color = [-1] * len(adjacency_list)
    # degree_buckets = defaultdict(list)

    # for node in sorted(adjacency_list.keys(), key=lambda x: len(adjacency_list[x])):
    #     degree_buckets[len(adjacency_list[node])].append(node)

    pick_order = list(range(len(adjacency_list)))
    random.shuffle(pick_order) 

    # for bucket in degree_buckets.keys():
    #     pick_order = list(range(len(degree_buckets[bucket])))
    #     random.shuffle(pick_order)

    for node in pick_order:
        # node = degree_buckets[bucket][pick]
        colors_used = set()
        for neighbours in adjacency_list[node]:
            colors_used.add(color[neighbours])
        
        try_color = 0
        while try_color in colors_used:
            try_color+=1
        
        if color[node] != -1:
            raise Exception('Recoloring not allowed')
        color[node] = try_color
    return color


def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    node_count = int(parts[0])
    edge_count = int(parts[1])
    
    edges = []
    adjacency_list = defaultdict(set)
    degree_counter = defaultdict(int)
    for i in range(1, edge_count+1):
        parts = list(map(int, lines[i].split()))
        edges.append([parts[0], parts[1]])
        adjacency_list[parts[0]].add(parts[1])
        adjacency_list[parts[1]].add(parts[0])
    
    for i in range(node_count):
        if i not in adjacency_list:
            adjacency_list[i] = set()

    num_cores = multiprocessing.cpu_count()
    results = Parallel(n_jobs=num_cores)(delayed(solve_greedy)(adjacency_list) for i in range(500))
    solution = min(results, key=lambda x: max(x))
    obj = max(solution)

    # prepare the solution in the specified output format
    output_data = str(obj+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def generateMinizincDataFile(item_count, edges_count, maximum_degree, edges, data_file):
    tmpFile = open(data_file, 'w')
    out = ""
    out += "nbNodes = " + str(item_count)+ ";\n"
    out += "nbEdges = " + str(edges_count)+ ";\n"
    out += "maxDegrees = " + str(maximum_degree) + ";\n"
    out += "edges = ["
    for edge in edges:
        out += '|{0}, {1}'.format(edge[0]+1, edge[1]+1)

    out += "|];\n"
    tmpFile.write(out)
    tmpFile.close()

def extractSolution(stdout):
    lines = stdout.split(bytes('\n', 'UTF-8'))
    line = lines[0]
    assignments = list(map(int, line.split()))
    return assignments

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')