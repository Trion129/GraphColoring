include "globals.mzn";

% parameters
int: nbNodes;
int: nbEdges;
int: maxDegrees;
int: maxColors;
array[1..nbEdges, 1..2] of int: edges; 
array[1..nbNodes] of var 1..(maxDegrees+1): assignments;

% constraints
constraint forall (i in 1..nbEdges) (assignments[edges[i, 1]] != assignments[edges[i, 2]]);
constraint max(assignments) <= maxColors;
   
% objective
solve :: int_search(assignments, dom_w_deg, indomain_min)
minimize max(assignments);

% output directive
output [ show(assignments[s]) ++ " "| s in 1..nbNodes ];