import math
from VOBJ import createVector
from Chunk_Struct import ChunkSystem

INFINITY = float("inf")


class sNode:
    def __init__(self, pos, nType, isObst, hasVis, GG, GL, parent):
        self.Visited = hasVis
        self.heuristic_cost = GG
        self.G_Cost = GL
        self.x = pos[0]
        self.y = pos[1]
        self.pos = createVector(pos[0], pos[1])
        self.Neighbours = []
        self.parent = parent
        self.nType = nType

    def __repr__(self):
        return f'({self.x}, {self.y})'


class tempPoint:
    def __init__(self, x, y):
        self.pos = createVector(x, y)


class PathfindingBoard:
    def __init__(self, mapList: list, gw: int, cs: int):
        self.nodeStarts = []
        self.nodeEnd = None
        self.grid_size = gw
        self.cellSize = cs
        self.cellMap = mapList
        self.nodeGrid = ChunkSystem(cs)
        self.nodeArray = []
        self.enemyArray = []
        self.distance = lambda a, b: math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
        self.heuristic = lambda a, b: self.distance(a, b)
        self.createGrid()
        self.connect_nodes()

    def __find_node_by_coord(self, x, y):  # arr: nodeGrid, param: set(x, y)
        for idx, node in enumerate(self.nodeGrid):
            cell = createVector(node.x // self.cellSize, node.y // self.cellSize)
            if [cell.x, cell.y] == [x, y]:
                return idx
        return False

    def createGrid(self) -> None:
        """
        Converts all cells in map to nodes for pathfinding
        :param cellMap: List of all cells in map
        """
        for idx, cell in enumerate(self.cellMap):

            x, y = (idx % self.grid_size) * self.cellSize, (idx // self.grid_size) * self.cellSize

            if cell != 2:
                nodeOBJ = sNode((x + self.cellSize/2, y + self.cellSize/2), 0, False, False, 0.0, 0.0, None)
                self.nodeGrid.insert(nodeOBJ)
                self.nodeArray.append(nodeOBJ)

    def connect_nodes(self):
        """
        Loops over all nodes and adds neighbours to walkable nodes
        """
        for idx, node in enumerate(self.nodeArray):

            temp = []
            temp.extend(self.nodeGrid.Query(tempPoint(node.x, node.y - self.cellSize), 0))
            temp.extend(self.nodeGrid.Query(tempPoint(node.x + self.cellSize, node.y), 0))
            temp.extend(self.nodeGrid.Query(tempPoint(node.x, node.y + self.cellSize), 0))
            temp.extend(self.nodeGrid.Query(tempPoint(node.x - self.cellSize, node.y), 0))
            node.Neighbours.extend(temp)

    def Solve_AStar(self, node_Start):
        """
        calculates the shortest path between two sNode objects and stores in parent node from endNode
        """
        for _, node in enumerate(self.nodeArray):  # reset all nodes back to default stats
            node.Visited = False
            node.heuristic_cost = INFINITY
            node.G_Cost = INFINITY
            node.parent = None

        # set basic data about start node
        currentNode = node_Start
        node_Start.heuristic_cost = self.heuristic(node_Start, self.nodeEnd)  # calculate starting heuristic
        node_Start.G_Cost = 0.0

        NodesToBeTested = [node_Start]  # list to store nodes still to be tested

        while len(NodesToBeTested) > 0:  # while there are nodes to test
            NodesToBeTested.sort(key=lambda x: x.heuristic_cost, reverse=True)  # sort based on heuristic cost attribute

            while len(NodesToBeTested) > 0 and NodesToBeTested[0].Visited:  # delete nodes that have been visited
                NodesToBeTested.pop(0)

            if len(NodesToBeTested) == 0: break

            currentNode = NodesToBeTested[0]
            currentNode.Visited = True

            # iterate over each nodes neighbor
            for _, nodeNeighbour in enumerate(currentNode.Neighbours):
                if not nodeNeighbour.Visited:  # if the node nodeNeighbour is yet to be visited
                    NodesToBeTested.append(nodeNeighbour)  # add to list of nodes to be tested

                PossiblyLowerGoal = currentNode.G_Cost + self.distance(currentNode, nodeNeighbour)  # calculated neighbour heuristic

                if PossiblyLowerGoal < nodeNeighbour.G_Cost:  # if neighbour is better option
                    nodeNeighbour.parent = currentNode  # parent to current node for working back through path
                    nodeNeighbour.G_Cost = self.heuristic(nodeNeighbour, self.nodeEnd)

    def getPath(self) -> list:
        """
        returns a list of coordinates for the enemy to travel to.
        """
        path = []

        if self.nodeEnd is not None:
            p = self.nodeEnd
            while p.parent is not None:
                path.append((p.x, p.y))
                p = p.parent
                if p.parent: p.type = 4

        return path[::-1][:-1]
