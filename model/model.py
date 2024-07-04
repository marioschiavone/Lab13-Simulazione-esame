import networkx as nx

from database.DAO import DAO
from geopy import distance


class Model:
    def __init__(self):

        self._allYears = DAO.getAllYears()
        self._allStates = DAO.getAllStates()
        self._idMap = {}
        """
        self._idMap={}
        for s in self._allStates:
            self._idMap[s.id] = s
        """
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self.pesoBest = 0
        self._bestPath = []

    def computePath(self):
        self._bestPath = []
        self.pesoBest = 0

        for node in self._grafo.nodes:
            parziale = [node]
            self._ricorsione(parziale, [])
        return self._bestPath, self.pesoBest

    def _ricorsione(self, parziale, edge_parziale):
        neighbors = self.getAdmissibleNeighbs(parziale[-1], edge_parziale)

        if len(neighbors) == 0:
            weight_path = self.computeWeightPath(edge_parziale)
            if weight_path > self.pesoBest:
                self.solBest = weight_path + 0.0
                self._bestPath = edge_parziale[:]
            return
        for n in neighbors:
            edge_parziale.append((parziale[-1], n, self._grafo.get_edge_data(parziale[-1], n)['weight']))
            parziale.append(n)

            self._ricorsione(parziale, edge_parziale)
            parziale.pop()
            edge_parziale.pop()

    def getAdmissibleNeighbs(self, last_node, edge_parziale):  # metto tutti i vicini con peso sempre maggiore
        result = []
        all_neigh = self._grafo.edges(last_node, data=True)
        for neighbor in all_neigh:
            if len(edge_parziale) != 0:
                if neighbor[2]["weight"] > edge_parziale[-1][2]:
                    result.append(neighbor[1])
            else:
                result.append(neighbor[1])
        return result

    def computeWeightPath(self, listOfNodes):
        weight = 0
        for e in listOfNodes:
            weight += distance.geodesic((e[0].Lat, e[0].Lng), (e[1].Lat, e[1].Lng)).km
        return weight

    def get_distance_weight(self, e):  # mi serve per calcolare la distanza quando stampo
        return distance.geodesic((e[0].Lat, e[0].Lng), (e[1].Lat, e[1].Lng)).km

    def buildGraph(self, y, s):
        self._grafo.clear()
        self._allSightings = DAO.getAllSightings(y, s)
        for sigh in self._allSightings:
            self._idMap[sigh.id] = sigh
            self._nodes.append(sigh)
        self._grafo.add_nodes_from(self._nodes)

        for n in range(len(self._nodes) - 1):
            current_sighting_id = (self._idMap[self._nodes[n].id])
            next_sighting_id = (self._idMap[self._nodes[n+1].id])
            self._grafo.add_edge(current_sighting_id,next_sighting_id)

        """
        for state in self._allStates:
            self._nodes.append(state)
        self._grafo.add_nodes_from(self._nodes)
        #allWeightedNeigh= DAO.getAllWeightedNeigh(a, s)
        allWeightedNeigh = DAO.getAllWeightedNeighV2(a1, a2, xG)
        for n in allWeightedNeigh:
            self._edges.append((self._idMap[n[0]], self._idMap[n[1]], n[2]))
        self._grafo.add_weighted_edges_from(self._edges)
        """

    def getSumWeightNeigh(self):
        pp = []
        for n in self._nodes:
            sum = 0
            for edge in self._grafo.edges(n, data=True):
                sum += edge[2]["weight"]
            pp.append((n.id, sum))
        return pp

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)
