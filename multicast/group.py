class Node:
    def __init__(self,id,addr,port):
        self.node_id=id
        self.addr=addr
        self.port=port

class NodeGroup:
    def __init__(self,selfNodeID, selfNodeAddr, selfNodePort,  Members):
        self.selfNodeId=selfNodeID
        self.selfNodeAddr=selfNodeAddr
        self.selfNodePort=selfNodePort
        self.members=Members

    