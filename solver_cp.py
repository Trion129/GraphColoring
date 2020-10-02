#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE
from collections import namedtuple, defaultdict

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    edge_count = int(parts[1])
    
    edges = []
    degree_counter = defaultdict(int)
    for i in range(1, edge_count+1):
        parts = lines[i].split()
        edges.append([int(parts[0]), int(parts[1])])
        degree_counter[parts[0]] += 1
        degree_counter[parts[1]] += 1

    maximum_degree = max(degree_counter.values())

    solved = False
    constraint = 1
    while not solved:
        print(constraint)
        # generate MiniZinc data file
        data_file = "data.dzn"
        generateMinizincDataFile(item_count, edge_count, maximum_degree, edges, constraint, data_file)

        # specify here how many solutions the solver should maximally search for ('0' means all)
        nb_solutions = 1

        # solve with Minizinc's MIP solver (CBC of COIN-OR)
        process = Popen(['minizinc.exe', '--solver', 'gecode', '--solver-time-limit', '120000','model.mzn', 'data.dzn'],
                    stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = process.communicate()

        # print error messages if there are any 
        if len(stderr) > 0:
            print(stderr)
            constraint += 1
            continue
        
        print(stdout)
        if bytes("=====UNSATISFIABLE=====", 'UTF-8') not in stdout:
            solved = True
            # extract the solution from standard-out
            solution = extractSolution(stdout)
        constraint += 1

    # calculate the cost of the solution
    obj = max(solution);

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

def generateMinizincDataFile(item_count, edges_count, maximum_degree, edges, constraint, data_file):
    tmpFile = open(data_file, 'w')
    out = ""
    out += "nbNodes = " + str(item_count)+ ";\n"
    out += "nbEdges = " + str(edges_count)+ ";\n"
    out += "maxDegrees = " + str(maximum_degree) + ";\n"
    out += "maxColors = " + str(constraint) + ";\n"
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