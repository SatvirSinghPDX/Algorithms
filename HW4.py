import math
import sys

#Class for verticies, in this case cities.
class Vertex(object):
    #defining initializer.
    def __init__(self, node):
        self.id = node
        self.value = math.inf
        self.adjacent = {} #dictionary to keep track of adjacent verticies.

    #defining self.
    def __str__(self):
        return str(self.id) + 'adjacent: ' + str([x.id for x in self.adjacent])

    #add neighbors to a vertex, store in adjacent dictionary and assign weight
    #to that neighbor.
    def addNeighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    #returns all neighbors in adjacency list
    def getConnections(self):
        return self.adjacent.keys()

    #returns value of a Vertex
    def getValue(self):
        return self.value

    #set value of a Vertex
    def setValue(self, val):
        self.value = val

    #returns id of a vertex
    def getId(self):
        return self.id

    #returns weight of edge between self and neighbor
    def getWeight(self, neighbor):
        return self.adjacent[neighbor]

#Class for the graph data structure
class Graph:
    #defining initializer
    def __init__(self):
        #A dictionary that maps vertex names to vertex objects
        self.vertDict = {}
        self.numVertices = 0

    #allows us to iterate over all the vertex objects in a graph
    def __iter__(self):
        return iter(self.vertDict.values())

    #add a vertex to the Graph
    def addVertex(self, node):
        if node not in self.vertDict:
            self.numVertices = self.numVertices + 1
            newVertex = Vertex(node)
            self.vertDict[node] = newVertex
            return newVertex

    #get a vertex in the graph
    def getVertex(self, n):
        if n in self.vertDict:
            return self.vertDict[n]
        else:
            return None #vertex not in graph

    #add edge between two verticies
    def addEdge(self, frm, to, cost = 0):
        if frm not in self.vertDict:
            self.addVertex(frm)
        if to not in self.vertDict:
            self.addVertex(to)

        #when adding neighbor, default weight is 0
        self.vertDict[frm].addNeighbor(self.vertDict[to], cost)
        self.vertDict[to].addNeighbor(self.vertDict[frm], cost)

    #return if a vertex is in Graph
    def inGraph(self, v):
        if v in self.vertDict:
            return True
        else:
            return False

    #get verticies of a Graph
    def getVerts (self):
        return self.vertDict.keys()

    #updates vertex value in Graph
    def updateVal(self, key, val):
        self.vertDict[key].setValue(val)

    #find vertex in graph with minimum value (not in MST and min value)
    def findMin(self, MST):
        min = math.inf

        for v in self.getVerts():
            if self.vertDict[v].getValue() < min and v not in MST.getVerts():
                min = self.vertDict[v].getValue()
                minV = self.getVertex(v)

        return minV

#Prim's MST implementation
def prim(g, firstWord):
        MST = Graph()
        prev = firstWord
        visited = []

        g.updateVal(firstWord,0)
        while (len(MST.getVerts()) != len(g.getVerts())):
            v = g.findMin(MST)
            MST.addVertex(v.getId())
            MST.updateVal(v.getId(), v.getValue())
            if (MST.inGraph(v.getId()) and MST.inGraph(prev) and prev != v.getId()):
                    if ({v.getId(), prev} not in visited):
                        MST.addEdge(prev, v.getId(), v.getValue())
                        prev = v.getId()
                        visited.append({v.getId(), prev})
            for u in v.getConnections():
                if u.getValue() > 0 and u.getWeight(v) < u.getValue(): #and not MST.inGraph(u):
                    g.updateVal(u.getId(), u.getWeight(v))


        printGraph(MST)

#Class to read information into graph frmfile
def readFile(fileName, g):
    with open(fileName, 'r') as f:
        for line in f:
            x = line.split()
            g.addVertex(x[0])
            g.addVertex(x[1])
            g.addEdge(x[0], x[1], int(x[2]))

    f=open(fileName)
    line = f.readline()
    x = line.split()
    return x[0]

#print graph
def printGraph(g):
    dist = 0
    visited = []
    for v in g:
        for w in v.getConnections():
            vId = v.getId()
            wId = w.getId()
            if ({vId, wId} not in visited):
                print (vId, "-", wId, ":", v.getWeight(w))
                visited.append({vId,wId})
                dist+=v.getWeight(w)
                print ('Cumulative distance:',str(dist), '\n')

    print ('Total distance of MST:', str(dist))

#Used to test the algorithm for correctness.
def generateTest(g):
    g.addVertex('A')
    g.addVertex('B')
    g.addVertex('C')
    g.addVertex('D')
    g.addVertex('E')
    g.addVertex('F')
    g.addVertex('G')
    g.addVertex('H')
    g.addVertex('I')

    g.addEdge('A', 'B', 4)
    g.addEdge('B', 'C', 8)
    g.addEdge('C', 'D', 7)
    g.addEdge('D', 'E', 9)
    g.addEdge('E', 'F', 10)
    g.addEdge('D', 'F', 14)
    g.addEdge('C', 'F', 4)
    g.addEdge('C', 'I', 2)
    g.addEdge('F', 'G', 2)
    g.addEdge('G', 'H', 1)
    g.addEdge('H', 'I', 7)
    g.addEdge('G', 'I', 6)
    g.addEdge('H', 'A', 8)
    g.addEdge('H', 'B', 11)

def main():
    g = Graph() #graph to hold cities and weights
    fileName = sys.argv[1] #where argv[1] is the file name of the cities
    firstWord = readFile(fileName, g)
    #generateTest(g)

    prim(g, firstWord)

if __name__ == '__main__':
    main()
