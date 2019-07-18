import networkx as nx

class HeterogeneousNetwork:
    def __init__(self):
        net=nx.Graph()
        self.net=net
        self.cache=False
        
    def setMemoryCache(self,b):
        self.memoryCache=b
        self.cache = {}

    def addNode(self,nodeKey,layer):
        self.net.add_node(nodeKey,layer=layer)
        
    def addEdge(self,nodeKey1,nodeKey2,weight):
        self.net.add_edge(nodeKey1,nodeKey2,weight=weight)
        
    def getNeighbors(self,nodeKey):
        
        if(self.memoryCache==True):
            if 'neighbors' in self.cache:
                if nodeKey in self.cache['neighbors']:
                    return self.cache['neighbors'][nodeKey]
        
        a = []
        for node in self.net.neighbors(nodeKey):
            a.append(node)
            
        if(self.memoryCache==True):
            if 'neighbors' not in self.cache: self.cache['neighbors']={}
            self.cache['neighbors'][nodeKey]=a
            
        return a
    
    def getNodes(self):
        return list(self.net.nodes)
    
    def setNodeData(self,nodeKey,key,value):
        self.net.nodes[nodeKey][key]=value
    
    def getNodeData(self,nodeKey,key):
        if key not in self.net.nodes[nodeKey]: return None
        return self.net.nodes[nodeKey][key]
    
    def getDegree(self,nodeKey):
        return len( self.getNeighbors(nodeKey) )
    
    def printNodes(self):
        print(self.net.nodes(data=True))
        
    def printEdges(self):
        print(self.net.edges(data=True))
        
    def loadCSV(self,csvFile):
        counter=1
        with open(csvFile) as myfile:
            for line in myfile:  
                data = line.split('\t')
                if(len(data)!=3):
                    print("Warning: malformed data in line "+str(counter)+" ["+line+"]")
                    continue

                ln = data[0].split(':')
                node1 = data[0].strip()
                node1_layer = ln[1].strip()

                ln = data[1].split(':')
                node2 = data[1].strip()
                node2_layer = ln[1].strip()

                weight = float(data[2].strip())
                
                self.addNode(node1,node1_layer)
                self.addNode(node2,node2_layer)
                self.addEdge(node1,node2,weight)
                
                counter+=1
    



