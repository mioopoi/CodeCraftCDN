import networkx as nx


def read_graph(file_name):
    G = nx.DiGraph()

    #f = open('data_copy/mid/case1.txt')
    f = open('data_copy/high/' + file_name)

    first_line = f.readline()
    #print first_line
    node_num, edge_num, cus_node_num = first_line.split()
    node_num, edge_num, cus_node_num = int(node_num), int(edge_num), int(cus_node_num)

    second_line = f.readline()  # blank

    open_cost = f.readline()
    #open_cost = int(open_cost)
    open_cost = 1000

    line = f.readline()  # blank

    for i in range(edge_num):
        line = f.readline()
        src, des, cap, fee = line.split()
        src, des, cap, fee = int(src), int(des), int(cap), int(fee)
        G.add_edge(src, des, cost = fee, capacity = cap)
        G.add_edge(des, src, cost = fee, capacity = cap)

    line = f.readline()

    for i in range(node_num):
        G.add_node(i, demand = 0)

    cus_list = []
    total_demand = 0
    for i in range(cus_node_num):
        line = f.readline()
        cus_node, adj_net_node, need = line.split()
        cus_node, adj_net_node, need = int(cus_node), int(adj_net_node), int(need)
        cus_list.append(adj_net_node)
        total_demand += need
        G.add_node(adj_net_node, demand = -need)

    f.close()

    print "number of nodes: %d" % G.number_of_nodes()
    print "number of edges: %d" % G.number_of_edges()
    print "number of customers: %d" % cus_node_num
    print "cost of server: %d" % open_cost

    return open_cost, cus_list, total_demand, G

#read_graph()