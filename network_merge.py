import csv

edges_list = []
nodes_list = []

#read in the edges network
with open('edges.txt', newline = '') as edges:
    edge_reader = csv.DictReader(edges, delimiter='\t')
    for edge in edge_reader:
        edges_list.append(dict(edge))
    #print(str(edges_list[1]['target'])+'\n')
    
#read in the nodes network
with open('nodes.txt', newline = '') as nodes:
    node_reader = csv.DictReader(nodes, delimiter='\t')
    for node in node_reader:
        nodes_list.append(dict(node))
    #print(str(nodes_list[0]['weight'])+'\n')
    
    
prev_id = ''
node_pos = 0

#fuuuuuuse them together
for i in range(len(edges_list)):
    print(node_pos)
    if i != 0:
        #check what channel we were last on in the edge list
        prev_id = edges_list[i-1]['source']
        print(prev_id)
        #if we've changed channels in the edge list, move one down the node list 
        if not prev_id == edges_list[i]['source']:
            node_pos += 1
    #update the edge_list with the node info (name and weight)
    edges_list[i].update(nodes_list[node_pos])
            
    print(str(edges_list[i])+'\n')
    
f = open('nodes_edges_merged.txt', 'w')
f.write('source\ttarget\tinteraction\tdirected\tname\tweight\n') 
#write the info we need, minus redundancies, to the new network file
for i in range(len(edges_list)):
    f.write(str(edges_list[i]['source']) + '\t' + str(edges_list[i]['target']) + '\t' + str(edges_list[i]['interaction']) + '\t' + str(edges_list[i]['directed']) + '\t' + str(edges_list[i]['name']) + '\t' + str(edges_list[i]['weight']) +'\n')
f.close()