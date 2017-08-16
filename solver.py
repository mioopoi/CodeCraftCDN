from gurobipy import *

from read_graph import read_graph

class ILPSolver:

    def __init__(self, f):
        self.open_cost, self.cus_list, self.tol_demand, self.graph = read_graph(f)
        self.n = self.graph.number_of_nodes()
        self.m = self.graph.number_of_edges()
        self.cus_num = len(self.cus_list)

        # Add "super source"
        source = self.n
        self.graph.add_node(source, demand = self.tol_demand)
        for i in range(self.n):
            self.graph.add_edge(source, i, cost = 0, capacity = 1000000)

        self.x = {}  # Open server decision variables: x[j] == 1 if node j is deployed with a server
        self.f = {}  # f[i,j] means the flow in edge (i,j) (Decision Variables)
        self.c = {}  # c[i,j] means the cost of edge (i,j)
        self.u = {}  # u[i,j] means the capacity of edge (i,j)
        self.b = {}  # b[i] means the demand of node i

    def solve(self):

        model = Model("CodeCraftCDN")

        print "Create models..."

        # Add variables
        for j in range(self.n):
            self.x[j] = model.addVar(vtype=GRB.BINARY, name="x%d" % j)

        for i in range(self.n + 1):
            self.b[i] = self.graph.node[i]['demand']
            #if (self.b[i] != 0):
            #    print self.b[i],
            for edge in self.graph.out_edges(i):
                self.c[edge] = self.graph.get_edge_data(edge[0], edge[1])['cost']
                self.u[edge] = self.graph.get_edge_data(edge[0], edge[1])['capacity']
                self.f[edge] = model.addVar(lb=0, ub=self.u[edge], vtype=GRB.INTEGER, name="f%d,%d" % (edge[0], edge[1]))
        model.update()

        # Add constraints

        # Supply/demand constraints
        for i in range(self.n + 1):
            in_edges = self.graph.in_edges(i)
            in_adj_nodes = []
            for edge in in_edges:
                in_adj_nodes.append(edge[0])

            model.addConstr( quicksum(self.f[i,j] for j in self.graph.adjacency_list()[i]) -
                             quicksum(self.f[j,i] for j in in_adj_nodes) == self.b[i] )

        # Open and flow constraints
        for edge in self.graph.out_edges(self.n):
            model.addConstr( self.f[edge] >= self.x[edge[1]] )
            model.addConstr( self.f[edge] <= self.u[edge] * self.x[edge[1]] )
            #self.f[edge] = model.addVar(lb=self.x[edge[1]], ub=self.u[edge]*self.x[edge[1]], vtype=GRB.INTEGER)

        model.update()

        # Set objective
        model.setObjective(
            self.open_cost * quicksum( self.x[j] for j in range(self.n) ) +
            quicksum( self.c[edge] * self.f[edge] for edge in self.graph.edges() ),
            GRB.MINIMIZE
        )

        model.setParam(GRB.Param.TimeLimit, 7200.0)
        model.update()

        print "Start optimizing..."
        model.optimize()

        solution = model.getAttr('x', self.x)
        server = []
        for j in range(self.n):
            if (solution[j]):
                server.append(j)
                print j,
        print

        return model.objVal, server


#solver = ILPSolver()
#obj = solver.solve()
#print obj
