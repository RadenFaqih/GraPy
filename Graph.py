import Node
import threading
#The graph object contains a bunch of nodes and is responsible for maintaining
#the datastructure of nodes. and having physics act upon them

#the main datastructure is a dictionary of nodes. where the key is the UID and the value is the node
#the other datastructure is of all of the relationships.
#this datastructure uses the UID as a key
#the value is a list like this[[outgoingrelationships as UIDs], [incomingrelationships as UIDs]]

class Graph:
    
    #these will be accessed as properties so that we can check if they are locked properly
    nodes = {}
    relationships = {}

    _locked = False
    _operating = False

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False

    def _safetycheck(self):
        while self._locked:
            pass

    def addNode(self, node):
        self._safetycheck()
        self._addNode(node)

    def _addNode(self, node):        
        if node.UID in self.nodes:
            self.removeNode(node.UID)

        self.nodes[node.UID] = node
        self.relationships[node.UID] = [[],[]]


    def removeNode(self, nodeID):
        self._safetycheck()
        self._removeNode(nodeID)

    #takes the ID of a node to remove
    def _removeNode(self, nodeID):
        if not nodeID in self.nodes:
            print "TRIED TO REMOVE NODE", nodeID, "WHICH DIDN'T EXIST."
            return

        #locking the dictionaries so we don't run in to errors
        
        for outgoingrelation in self.relationships[nodeID][0]:
            self.removeRelationship(nodeID, outgoingrelation)
            #relationships[outgoingrelation][1].remove(node.UID)

        for incomingrelation in self.relationships[nodeID][1]:
            self.removeRelationship(incomingrelation, nodeID)
            #relationships[incomingrelation][0].remove(node.UID)

        del self.relationships[nodeID]
        del self.nodes[nodeID]

    def removeRelationship(self, outgoing, incoming):
        self._safetycheck()
        self.removeRelationship(outgoing, incoming)

    #takes the IDs of the outgoing and imconing nodes
    def _removeRelationship(self, outgoing, incoming):
        if (not outgoing in self.relationships):
            print "TRIED TO REMOVE RELATIONSHIP", outgoing, " > ", incoming, "WHEN OUTGOING DIDN'T EXIST."
            return
        if (not incoming in self.relationships):
            print "TRIED TO REMOVE RELATIONSHIP", outgoing, " > ", incoming, "WHEN INCOMING DIDN'T EXIST."
            return
        
        self.relationships[outgoing][0].remove(incoming)
        self.relationships[incoming][1].remove(outgoing)

    def addRelationship(self, outgoing, incoming):
        self._safetycheck()
        self._addRelationship(outgoing, incoming)

    def _addRelationship(self, outgoing, incoming):
        if (not outgoing in self.relationships):
            print "TRIED TO ADD RELATIONSHIP", outgoing, " > ", incoming, "WHEN OUTGOING DIDN'T EXIST."
            return
        if (not incoming in self.relationships):
            print "TRIED TO ADD RELATIONSHIP", outgoing, " > ", incoming, "WHEN INCOMING DIDN'T EXIST."
            return
        
        self.relationships[outgoing][0] = self.relationships[outgoing][0] + [incoming]
        self.relationships[incoming][1] = self.relationships[incoming][1] + [outgoing]

    #the function that does all of the physics calculations. timeinterval is in miliseconds
    #we do the following things:
        #calculate and apply attractive forces
        #calculate and apply repulsive forces
        #move each node
    def doPhysics(self, timeinterval):
        self.calculateAttractiveForces()
        self.calculateRepulsiveForces()

        self.moveAllNodes(timeinterval)

    #we go through every outgoing relationship, and for each one apply a force to both the outgoing node and incoming
    def calculateAttractiveForces(self):
        for nodeUID in self.relationships:
            for outgoingrelationUID in self.relationships[nodeUID][0]:
                #print "calculating an attractive force for node", nodeUID
                fx, fy = self.nodes[nodeUID].calculateAttractiveForce(self.nodes[outgoingrelationUID])
                #print fx, fy
                self.nodes[nodeUID].applyForce((fx, fy))
                self.nodes[outgoingrelationUID].applyForce((-fx, -fy))

    #right now this method calculates repulsive forces for all nodes on the graph, but in future
    #a goood optimisation is only to calculate it for the closest nodes
    def calculateRepulsiveForces(self):
        for n in self.nodes.values():
            for m in self.nodes.values():
                if n == m:
                    continue
                n.applyForce(n.calculateRepulsiveForce(m))

    #applies each node's forces to it
    def moveAllNodes(self, timeinterval):
        for n in self.nodes.values():
            n.move(timeinterval)
